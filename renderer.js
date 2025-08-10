"use strict";

// requires
const { remote, ipcRenderer, shell } = require('electron')
const { BrowserWindow, dialog } = remote
const util = require('util')
const fs = require('fs')
const path = require('path')
var sizeOf = require('image-size')

// main
const clusters = require('./clusters.json')
main()

// functions
async function main() {
    addKeyboardShortcuts()
    showSidebarThumbnails()
}

function addKeyboardShortcuts() {
    document.addEventListener('keyup', function (event) {
        if (event.keyCode == 8) {
            deleteCurrentImage()
        }
    })
}

function closeWindow() {
    let window = remote.getCurrentWindow()
    window.close()
}

function getFirstImage(cluster) {
    let keys = Object.keys(cluster)
    if (keys.length > 0) {
        return keys[0]
    }
}

function showSidebarThumbnails() {
    let sidebar = getSidebar()
    sidebar.innerHTML = ""
    for (let i = 0; i < clusters.length; i++) {
        let imagePath = getFirstImage(clusters[i])
        let t = newThumbnail(imagePath, "vertical", () => showCluster(i))
        sidebar.append(t)
    }
    showCluster(0)
}

function getSidebar() {
    return document.getElementById("sidebar")
}

function getDownbar() {
    return document.getElementById("image-thumbs")
}

function showCluster(num) {
    setActiveThumbnailNum(getSidebar(), num)
    showClusterThumbnails(clusters[num])
}

function showClusterThumbnails(cluster) {
    let downbar = getDownbar()
    let imagePaths = Object.keys(cluster)
    showThumbnails(downbar, "horizontal", imagePaths, showImage, cluster)
}

function showThumbnails(element, orientation, imagePaths, showFunction, cluster) {
    element.innerHTML = ""
    for (let imagePath of imagePaths) {
        let imageDetails = cluster[imagePath]
        let t = newThumbnail(imagePath, orientation, () => showFunction(imagePath, imageDetails))
        element.append(t)
    }
    if (imagePaths.length > 0) {
        showFunction(imagePaths[0], cluster[imagePaths[0]])
    }
}

function newThumbnail(imagePath, orientation, showFunction) {
    let e = newImage(imagePath)
    e.addEventListener("click", showFunction)
    let t = document.createElement("div")
    t.className = "thumbnail " + orientation
    t.appendChild(e)
    return t
}

function newImage(path) {
    let e = document.createElement("img")
    e.setAttribute("src", path)
    return e
}

function setActive(thumbnail, state) {
    thumbnail.setAttribute("data-active", state)
}

function getImageContainer() {
    return document.getElementById("content-image")
}

function showImage(imagePath, difference) {
    let e = getImageContainer()
    e.innerHTML = ""
    e.appendChild(newImage(imagePath))
    setActiveThumbnail(getDownbar(), imagePath)
    let { width, height } = sizeOf(imagePath);
    let stats = fs.statSync(imagePath)
    let size = stats["size"]
    let sizeMiB = size/2**20
    let info = document.getElementById("content-bottom")
    let string = `${width} &times; ${height} px &mdash; ${sizeMiB.toFixed(3)} MiB &mdash; Difference: ${difference}`
    info.innerHTML = string
    let content = document.getElementById("content-top")
    content.innerHTML = `<div>${imagePath}</div><div class="help-text">Press <kbd>← backspace</kbd> to move this file to the trash bin.<div>`
}

function setActiveThumbnail(container, path) {
    for (let e of container.childNodes) {
        let img = e.firstChild
        setActive(e, img.getAttribute("src") == path)
    }
}

function setActiveThumbnailNum(container, num) {
    let children = container.childNodes
    for (let i = 0; i < children.length; i++) {
        let e = children[i]
        let img = e.firstChild
        setActive(e, i == num)
    }
}

function deleteCurrentImage() {
    let path = getCurrentImage()
    if (path) {
        let num = getSelectedCluster()
        let deleted = deleteFile(path)
        if (deleted) {
            removeImageFromAllClusters(path)
            showCluster(num)
        }
    }
}

function getCurrentImage() {
    let e = getImageContainer()
    return e.firstChild.getAttribute("src")
}

function getSelectedCluster() {
    let container = getSidebar()
    let children = container.childNodes
    for (let i = 0; i < children.length; i++) {
        let e = children[i]
        let img = e.firstChild
        if (e.getAttribute("data-active") == "true") {
            return i
        }
    }
}

function removeImageFromAllClusters(path) {
    for (let i = 0; i < clusters.length; i++) {
        if (path in clusters[i]) {
            delete clusters[i][path]
            updateSidebarImage(i)
            if (Object.keys(clusters[i]).length <= 1) {
                // cluster contains 1 or no images
                hideClusterInSidebar(i)
            }
        }
    }
}

function hideClusterInSidebar(num) {
    let container = getSidebar()
    let thumbnail = getSidebar().childNodes[num]
    thumbnail.setAttribute("data-hidden", true)
}

function updateSidebarImage(num) {
    let imagePath = getFirstImage(clusters[num])
    let container = getSidebar()
    let thumbnail = container.childNodes[num]
    let img = thumbnail.firstChild
    if (imagePath) {
        img.setAttribute("src", imagePath)
    } else {
        img.setAttribute("src", "")
    }
}

function deleteFile(path) {
    let deleted = shell.moveItemToTrash(path)
    if (!deleted) {
        alert(`The file ${path} could not be deleted.`)
    }
    return deleted
}
