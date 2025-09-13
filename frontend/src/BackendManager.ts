import { Notice } from 'obsidian';
import { spawn, ChildProcess } from 'child_process';
import * as path from 'path';
import * as fs from 'fs';

export class BackendManager {
    private backendProcess: ChildProcess | null = null;
    private readonly pluginPath: string;
    private readonly executableName: string;
    private readonly executablePath: string;
    private readonly serverUrl: string = 'http://localhost:8000';
    private isStarting: boolean = false;

    constructor(pluginPath: string) {
        this.pluginPath = pluginPath;
        this.executableName = process.platform === 'win32' ? 'documize-backend.exe' : 'documize-backend';
        this.executablePath = path.join(pluginPath, 'dist', this.executableName);
    }

    /**
     * Backend 서버가 실행 중인지 확인
     */
    async isServerRunning(): Promise<boolean> {
        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 3000); // 3초로 단축
            
            const response = await fetch(`${this.serverUrl}/health`, {
                method: 'GET',
                signal: controller.signal,
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                }
            });
            
            clearTimeout(timeoutId);
            
            if (response.ok) {
                const data = await response.json();
                console.log('서버 헬스 체크 성공:', data);
                return true;
            } else {
                console.log(`서버 헬스 체크 실패: ${response.status} ${response.statusText}`);
                return false;
            }
        } catch (error) {
            if (error.name === 'AbortError') {
                console.log('서버 헬스 체크 타임아웃 (3초)');
            } else {
                console.log('서버 헬스 체크 오류:', error.message);
            }
            return false;
        }
    }

    /**
     * Backend 실행파일이 존재하는지 확인
     */
    isExecutableAvailable(): boolean {
        return fs.existsSync(this.executablePath);
    }

    /**
     * Logs 폴더 정리
     */
    private cleanupLogs(): void {
        const logsPath = path.join(this.pluginPath, 'logs');
        if (fs.existsSync(logsPath)) {
            try {
                fs.rmSync(logsPath, { recursive: true, force: true });
                console.log('Logs 폴더가 정리되었습니다.');
            } catch (error) {
                console.warn('Logs 폴더 정리 중 오류:', error);
            }
        }
    }

    /**
     * Backend 서버 시작
     */
    async startBackend(): Promise<boolean> {
        if (this.isStarting) {
            console.log('Backend가 이미 시작 중입니다.');
            return false;
        }

        if (this.backendProcess && !this.backendProcess.killed) {
            console.log('Backend가 이미 실행 중입니다.');
            return true;
        }

        if (!this.isExecutableAvailable()) {
            new Notice('Backend 실행파일을 찾을 수 없습니다. 먼저 빌드해주세요.');
            console.error(`Backend 실행파일이 없습니다: ${this.executablePath}`);
            return false;
        }

        // Logs 폴더 정리
        this.cleanupLogs();

        this.isStarting = true;

        try {
            console.log('Backend 서버 시작 중...');
            console.log(`실행파일 경로: ${this.executablePath}`);

            // Backend 프로세스 시작
            this.backendProcess = spawn(this.executablePath, [], {
                cwd: this.pluginPath,
                stdio: ['ignore', 'pipe', 'pipe'],
                detached: false
            });

            // 프로세스 이벤트 핸들러
            this.backendProcess.on('error', (error) => {
                console.error('Backend 프로세스 오류:', error);
                console.error('오류 상세:', {
                    name: error.name,
                    message: error.message,
                    stack: error.stack,
                    code: (error as any).code,
                    errno: (error as any).errno,
                    syscall: (error as any).syscall
                });
                new Notice(`Backend 시작 실패: ${error.message}`);
                this.isStarting = false;
            });

            this.backendProcess.on('exit', (code, signal) => {
                console.log(`Backend 프로세스 종료: code=${code}, signal=${signal}`);
                if (code !== 0) {
                    console.error(`Backend 프로세스가 비정상 종료되었습니다. 종료 코드: ${code}`);
                    new Notice(`Backend가 비정상 종료되었습니다 (코드: ${code})`);
                }
                this.backendProcess = null;
                this.isStarting = false;
            });

            // stdout/stderr 로그 처리
            if (this.backendProcess.stdout) {
                this.backendProcess.stdout.on('data', (data) => {
                    console.log('Backend stdout:', data.toString());
                });
            }

            if (this.backendProcess.stderr) {
                this.backendProcess.stderr.on('data', (data) => {
                    console.error('Backend stderr:', data.toString());
                });
            }

            // 서버가 완전히 시작될 때까지 대기
            await this.waitForServerStart();

            console.log('Backend 서버가 성공적으로 시작되었습니다.');
            new Notice('Backend 서버가 시작되었습니다.');
            return true;

        } catch (error) {
            console.error('Backend 시작 중 오류:', error);
            
            // 진단 정보 수집
            const issues = await this.diagnoseStartupFailure();
            console.error('시작 실패 진단:', issues);
            
            let errorMessage = `Backend 시작 실패: ${error.message}`;
            if (issues.length > 0) {
                errorMessage += `\n진단 정보: ${issues.join(', ')}`;
            }
            
            new Notice(errorMessage);
            this.isStarting = false;
            return false;
        }
    }

    /**
     * Backend 서버 중지
     */
    async stopBackend(): Promise<boolean> {
        if (!this.backendProcess || this.backendProcess.killed) {
            console.log('Backend가 실행 중이 아닙니다.');
            return true;
        }

        try {
            console.log('Backend 서버 중지 중...');
            
            // 프로세스 종료
            this.backendProcess.kill('SIGTERM');
            
            // 강제 종료를 위한 타임아웃
            setTimeout(() => {
                if (this.backendProcess && !this.backendProcess.killed) {
                    console.log('강제 종료 중...');
                    this.backendProcess.kill('SIGKILL');
                }
            }, 5000);

            // 프로세스가 완전히 종료될 때까지 대기
            await new Promise<void>((resolve) => {
                if (this.backendProcess) {
                    this.backendProcess.on('exit', () => {
                        resolve();
                    });
                } else {
                    resolve();
                }
            });

            this.backendProcess = null;
            console.log('Backend 서버가 중지되었습니다.');
            new Notice('Backend 서버가 중지되었습니다.');
            return true;

        } catch (error) {
            console.error('Backend 중지 중 오류:', error);
            new Notice(`Backend 중지 실패: ${error.message}`);
            return false;
        }
    }

    /**
     * 서버가 시작될 때까지 대기
     */
    private async waitForServerStart(maxAttempts: number = 30, interval: number = 1000): Promise<void> {
        console.log(`서버 시작 대기 중... (최대 ${maxAttempts}초)`);
        
        for (let i = 0; i < maxAttempts; i++) {
            try {
                if (await this.isServerRunning()) {
                    console.log(`서버가 ${i + 1}초 후에 성공적으로 시작되었습니다.`);
                    return;
                }
            } catch (error) {
                console.log(`서버 상태 확인 시도 ${i + 1}/${maxAttempts}: ${error.message}`);
            }
            
            // 프로세스가 종료되었는지 확인
            if (this.backendProcess && this.backendProcess.killed) {
                console.error('Backend 프로세스가 예상보다 일찍 종료되었습니다.');
                throw new Error('Backend 프로세스가 예상보다 일찍 종료됨');
            }
            
            if (i % 5 === 0 && i > 0) {
                console.log(`서버 시작 대기 중... (${i}/${maxAttempts}초 경과)`);
            }
            
            await new Promise(resolve => setTimeout(resolve, interval));
        }
        
        console.error('서버 시작 타임아웃: 서버가 예상 시간 내에 시작되지 않았습니다.');
        throw new Error(`서버 시작 타임아웃 (${maxAttempts}초)`);
    }

    /**
     * Backend 프로세스 상태 확인
     */
    isBackendRunning(): boolean {
        return this.backendProcess !== null && !this.backendProcess.killed;
    }

    /**
     * 서버 URL 반환
     */
    getServerUrl(): string {
        return this.serverUrl;
    }

    /**
     * 실행파일 경로 반환
     */
    getExecutablePath(): string {
        return this.executablePath;
    }

    /**
     * 서버 시작 실패 시 진단 정보 수집
     */
    async diagnoseStartupFailure(): Promise<string[]> {
        const issues: string[] = [];
        
        // 실행파일 존재 확인
        if (!this.isExecutableAvailable()) {
            issues.push(`실행파일이 없습니다: ${this.executablePath}`);
        } else {
            // 실행 권한 확인
            try {
                const fs = require('fs');
                const stats = fs.statSync(this.executablePath);
                if (!stats.isFile()) {
                    issues.push('실행파일이 파일이 아닙니다.');
                } else {
                    // 파일 크기 확인
                    if (stats.size === 0) {
                        issues.push('실행파일이 비어있습니다 (크기: 0바이트)');
                    }
                }
            } catch (error) {
                issues.push(`실행파일 접근 오류: ${error.message}`);
            }
        }
        
        // 포트 사용 확인
        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 1000);
            
            const response = await fetch(`${this.serverUrl}/health`, {
                method: 'GET',
                signal: controller.signal
            });
            
            clearTimeout(timeoutId);
            
            if (response.ok) {
                issues.push('포트 8000이 이미 사용 중입니다.');
            }
        } catch (error) {
            // 포트가 사용되지 않음 - 정상
        }
        
        // 프로세스 상태 확인
        if (this.backendProcess && !this.backendProcess.killed) {
            issues.push('Backend 프로세스가 이미 실행 중입니다.');
        }
        
        // 플러그인 경로 확인
        if (!fs.existsSync(this.pluginPath)) {
            issues.push(`플러그인 경로가 존재하지 않습니다: ${this.pluginPath}`);
        }
        
        // dist 폴더 확인
        const distPath = path.join(this.pluginPath, 'dist');
        if (!fs.existsSync(distPath)) {
            issues.push(`dist 폴더가 존재하지 않습니다: ${distPath}`);
        }
        
        return issues;
    }
}
