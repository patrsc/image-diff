"use strict";

// requires
const { remote, ipcRenderer } = require('electron')
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
    // ipcRenderer.on('update', updateFiles)
    addKeyboardShortcuts()
    showSidebarThumbnails(Object.keys(clusters))
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

function getSidebar() {
    return document.getElementById("sidebar")
}

function getDownbar() {
    return document.getElementById("image-thumbs")
}

function showCluster(refImage) {
    setActiveThumbnail(getSidebar(), refImage)
    let cluster = {[refImage]: 0, ...clusters[refImage]}
    showClusterThumbnails(cluster)
}

function showSidebarThumbnails(imagePaths) {
    let sidebar = getSidebar()
    showThumbnails(sidebar, "vertical", imagePaths, showCluster, clusters)
}

function showClusterThumbnails(cluster) {
    let downbar = getDownbar()
    let imagePaths = Object.keys(cluster)
    showThumbnails(downbar, "horizontal", imagePaths, showImage, cluster)
}

function showThumbnails(element, orientation, imagePaths, showFunction, details) {
    element.innerHTML = ""
    for (let i of imagePaths) {
        let imageDetails = details[i]
        let t = newThumbnail(i, orientation, showFunction, imageDetails)
        element.append(t)
    }
    showFunction(imagePaths[0], details[imagePaths[0]])
}

function newThumbnail(imagePath, orientation, showFunction, imageDetails) {
    let e = newImage(imagePath)
    e.addEventListener("click", () => showFunction(imagePath, imageDetails))
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
    let location = document.getElementById("content-top")
    location.innerHTML = imagePath
}

function setActiveThumbnail(container, path) {
    for (let e of container.childNodes) {
        let img = e.firstChild
        setActive(e, img.getAttribute("src") == path)
    }
}

function getActiveThumbnailPath(container) {
    for (let e of container.childNodes) {
        let img = e.firstChild
        if (e.getAttribute("data-active") == "true") {
            return img.getAttribute("src")
        }
    }
}

function getCurrentImage() {
    let e = getImageContainer()
    return e.firstChild.getAttribute("src")
}

function deleteCurrentImage() {
    let path = getCurrentImage()
    if (path) {
        console.log("Del: " + path)
        let refImage = getActiveThumbnailPath(getSidebar())
        console.log(refImage)
        delete clusters[refImage][path]
        console.log(clusters[refImage])
        showCluster(refImage)
        if (Object.keys(clusters[refImage]).length == 0) {
            console.log("rm cluster")
        }
    }
}
