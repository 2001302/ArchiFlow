const { app, BrowserWindow, ipcMain } = require('electron')
const path = require('path')

let mainWindow

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        },
        frame: false,
        backgroundColor: '#1E1E1E'
    })

    mainWindow.loadFile('src/index.html')
}

app.whenReady().then(createWindow)

// 윈도우 컨트롤 이벤트 핸들러
ipcMain.on('minimize-window', () => {
    mainWindow.minimize()
})

ipcMain.on('maximize-window', () => {
    if (mainWindow.isMaximized()) {
        mainWindow.unmaximize()
    } else {
        mainWindow.maximize()
    }
})

ipcMain.on('close-window', () => {
    mainWindow.close()
})

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit()
    }
})

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow()
    }
}) 