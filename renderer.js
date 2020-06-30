"use strict";

// requires
const { remote, ipcRenderer } = require('electron')
const { BrowserWindow, dialog } = remote
const util = require('util')
const fs = require('fs');
const path = require('path')

// promisified functions
const renameFile = util.promisify(fs.rename)

// main
main()

// functions
async function main() {
    // ipcRenderer.on('update', updateFiles)
    console.log("Hello")
}

function closeWindow() {
    let window = remote.getCurrentWindow()
    window.close()
}
