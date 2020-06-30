"use strict";

const { app, BrowserWindow, dialog } = require('electron')
const os = require('os')
const fs = require('fs-extra')

// Global reference to main window
let win

// Main
global.arguments = getArguments()

// macOS: open file event is emitted when user drops file/folder onto dock
app.on('open-file', function(event, path) {
    event.preventDefault()
    global.arguments.push(path)
    if (win != undefined) { // if the window is already open
        win.webContents.send('update')
    }
})

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(createWindow)

// Quit when all windows are closed.
app.on('window-all-closed', () => {
    // On macOS it is common for applications and their menu bar
    // to stay active until the user quits explicitly with Cmd + Q
    //if (process.platform !== 'darwin') {
        app.quit()
    //}
})

app.on('activate', () => {
    // On macOS it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    //if (BrowserWindow.getAllWindows().length === 0) {
    //    createWindow()
    //}
})

// functions
function createWindow () {
    // Create the browser window.
    win = new BrowserWindow({
        width: 900,
        height: 600,
        minWidth: 600,
        minHeight: 480,
        webPreferences: {
            nodeIntegration: true
        },
        backgroundColor: '#f3f3f3',
    })

    // and load the index.html of the app.
    win.loadFile('index.html')

    // Open the DevTools.
    /*win.webContents.openDevTools()
    win.webContents.on('devtools-opened', () => {
        win.webContents.focus()
    })*/
}

function getArguments() {
    var n = process.argv.indexOf('--') // use all arguments after '--'
    if (n == -1) {
        n = 0 // use all arguments after program name
    }
    return process.argv.slice(n + 1)
}

function logInWindow(win, message) {
    win.webContents.executeJavaScript(`console.log("${message}")`)
}
