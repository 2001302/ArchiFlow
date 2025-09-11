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
        this.executableName = process.platform === 'win32' ? 'arch-flow-backend.exe' : 'arch-flow-backend';
        this.executablePath = path.join(pluginPath, 'dist', this.executableName);
    }

    /**
     * Backend 서버가 실행 중인지 확인
     */
    async isServerRunning(): Promise<boolean> {
        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 2000);
            
            const response = await fetch(`${this.serverUrl}/health`, {
                method: 'GET',
                signal: controller.signal
            });
            
            clearTimeout(timeoutId);
            return response.ok;
        } catch (error) {
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
                new Notice(`Backend 시작 실패: ${error.message}`);
                this.isStarting = false;
            });

            this.backendProcess.on('exit', (code, signal) => {
                console.log(`Backend 프로세스 종료: code=${code}, signal=${signal}`);
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
            new Notice(`Backend 시작 실패: ${error.message}`);
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
        for (let i = 0; i < maxAttempts; i++) {
            if (await this.isServerRunning()) {
                return;
            }
            await new Promise(resolve => setTimeout(resolve, interval));
        }
        throw new Error('서버 시작 타임아웃');
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
}
