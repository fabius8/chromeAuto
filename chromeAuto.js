const axios=require('axios');
const puppeteer=require('puppeteer');
const net = require('net');
const path = require('path');
require("dotenv").config();

const currentDirectory = process.cwd();
const relateDirectory = "pproxy\\switchomega_bak\\"
const metamask_url = "chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html"

let metamask_password = process.env.METAMASK_PASSWORD
let portBase = 9200
let num1 = 1
let num2 = 300

const args = process.argv.slice(2);
const commandString = args[0];
const varSting1 = args[1]
const varSting2 = args[2]
const varSting3 = args[3]
console.log(commandString, varSting1, varSting2, varSting3)

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function randomSleep(min, max) {
    const range = max - min;
    const randomTime = Math.random() * range + min;
    return new Promise(resolve => setTimeout(resolve, randomTime));
}
function isPortTaken(port, host) {
    return new Promise((resolve) => {
      const server = net.createServer();
  
      server.once('error', (error) => {
        if (error.code === 'EADDRINUSE') {
          resolve(true);
        } else {
          resolve(false);
        }
      });
  
      server.once('listening', () => {
        server.close();
        resolve(false);
      });
  
      server.listen(port, host);
    });
}

if (commandString == "metamaskLogin"){
    console.log(commandString, "...")
    BatchMetamaskLogin()
}

async function BatchMetamaskLogin(){
    for(let i = num1; i <= num2; i++){
        let port = portBase + i
        let webSocketDebuggerUrl = "http://127.0.0.1:" + port + "/json/version"
        metamaskLogin(i, port, webSocketDebuggerUrl)
        //await sleep(100)
    }
}

async function metamaskLogin(index, port, webSocketDebuggerUrl){
    const result = await isPortTaken(port, '127.0.0.1')
    if (result) {
        console.log(index, result, port, "已启动！")
    }
    else {
        return
    }
    await randomSleep(1, 2000) 
    let wsKey = await axios.get(webSocketDebuggerUrl);
    let browser = await puppeteer.connect({
        browserWSEndpoint: wsKey.data.webSocketDebuggerUrl,
        defaultViewport:null
    });
    let page = await browser.newPage()
    const extensionUrl = metamask_url;
    await page.goto(extensionUrl, { waitUntil: 'load' });
    try{
        await sleep(100)
        var input = await page.waitForSelector('input[id=password]', {visible: true, timeout:3000})
        await input.type(metamask_password);
        await sleep(100)
        await Promise.all([
            page.keyboard.press('Enter'),
            page.waitForNavigation({waitUntil: 'load'})
        ]);
        console.log("第", index, "个", "metamask 已解锁！")
    }catch(e){
        console.log('e==>', e.message)
    }
    await sleep(1000)
    await browser.disconnect()
}

// 命令处理
if (commandString == "proxyLoad"){
    console.log(commandString, "...")
    BatchProxyConfigLoad()
}

async function BatchProxyConfigLoad(){
    for(let i = num1; i <= num2; i++){
        let port = portBase + i
        let webSocketDebuggerUrl = "http://127.0.0.1:" + port + "/json/version"
        proxyConfigLoad(i, port, webSocketDebuggerUrl)
        //await sleep(100)
    }
}

async function proxyConfigLoad(index, port, webSocketDebuggerUrl){
    const result = await isPortTaken(port, '127.0.0.1')
    if (result) {
        console.log(index, result, port, "已启动！")
    }
    else {
        return
    }
    let cfg_num = 10
    let num = index % cfg_num
    if (num == 0){
        num = cfg_num
    }
    let filepath = path.join(currentDirectory, relateDirectory, num.toString() + '.json');
    console.log(filepath)
    let wsKey = await axios.get(webSocketDebuggerUrl);
    let browser = await puppeteer.connect({
        browserWSEndpoint: wsKey.data.webSocketDebuggerUrl,
        defaultViewport:null,
    });

    let page = null
    while(true){
        try{
            page = await browser.newPage()
            await page.goto('chrome-extension://padekgcemlokbadohgkifijomclgjgif/options.html#!/io', { waitUntil: 'load' });
            //await page.click('button[ng-click="triggerFileInput()"] .ladda-label');
            // 等待文件选择框出现
            const inputElement = await page.$('input[type="file"]');    // 上传文件
            await inputElement.uploadFile(filepath);
            console.log(index, '文件上传完成！');
            await sleep(1000)
            await page.close()
            break
        }
        catch(e){
            console.log(index, e.message)
            await page.close()
            await sleep(5000)
        }
    }
    await browser.disconnect()
}

if (commandString == "open"){
    console.log(commandString, "...")
    batchOpenURL()
}

async function batchOpenURL(){
    for(let i = num1; i <= num2; i++){
        let port = portBase + i
        let webSocketDebuggerUrl = "http://127.0.0.1:" + port + "/json/version"
        openURL(i, port, webSocketDebuggerUrl)
        //await sleep(100)
    }
}

async function openURL(index, port, webSocketDebuggerUrl){
    const result = await isPortTaken(port, '127.0.0.1')
    if (result) {
        console.log(index, result, port, "已启动！")
    }
    else {
        return
    }
    await randomSleep(1, 2000) 
    let wsKey = await axios.get(webSocketDebuggerUrl);
    let browser = await puppeteer.connect({
        browserWSEndpoint: wsKey.data.webSocketDebuggerUrl,
        defaultViewport:null,
    });

    let page = await browser.newPage()
    try{
        await page.goto(varSting1, { waitUntil: 'load' });
        console.log(index, '网页打开成功！');
        await sleep(1000)
    }
    catch(e){
        console.log(e.message)
    }
    await browser.disconnect()
}



if (commandString == "argentLogin"){
    console.log(commandString, "...")
    argent()
}

async function argent(){
    for(let i = num1; i <= num2; i++){
        let port = portBase + i
        let webSocketDebuggerUrl = "http://127.0.0.1:" + port + "/json/version"
        argentLogin(i, port, webSocketDebuggerUrl)
        //await sleep(100)
    }
}

async function argentLogin(index, port, webSocketDebuggerUrl){
    const result = await isPortTaken(port, '127.0.0.1')
    if (result) {
        console.log(index, result, port, "已启动！")
    }
    else {
        return
    }

    let wsKey = await axios.get(webSocketDebuggerUrl);
    let browser = await puppeteer.connect({
        browserWSEndpoint: wsKey.data.webSocketDebuggerUrl,
        defaultViewport:null
    });
    let page = await browser.newPage()
    const extensionUrl = `chrome-extension://dlcobpjiigpikoobohmabehhmhfoodbb/index.html`;
    await page.goto(extensionUrl, { waitUntil: 'load' });
    try{
        await sleep(100)
        var input = await page.waitForSelector('input[name=password]', {visible: true, timeout:3000})
        await input.type(metamask_password);
        await sleep(100)
        await Promise.all([
            page.keyboard.press('Enter'),
            page.waitForNavigation({waitUntil: 'load'})
        ]);
        console.log("第", index, "个", "argentx 已解锁！")
    }catch(e){
        console.log('e==>', e.message)
    }
    await sleep(1000)
    await browser.disconnect()
}

if (commandString == "click"){
    console.log(commandString, "...")
    batchClickElement()
}

async function batchClickElement(){
    for(let i = num1; i <= num2; i++){
        let port = portBase + i
        let webSocketDebuggerUrl = "http://127.0.0.1:" + port + "/json/version"
        click(i, port, webSocketDebuggerUrl, varSting1, varSting2)
        //await sleep(100)
    }
}


async function click(index, port, webSocketDebuggerUrl, varSting1, varSting2) {
    const result = await isPortTaken(port, '127.0.0.1')
    if (result) {
        console.log(index, result, port, "已启动！")
    }
    else {
        return
    }

    let wsKey = await axios.get(webSocketDebuggerUrl);
    let browser = await puppeteer.connect({
        browserWSEndpoint: wsKey.data.webSocketDebuggerUrl,
        defaultViewport:null
    });
    while (true) {
        try{
            const pages = await browser.pages();
            let currentPage
            for (let i = 0; i < pages.length; i++) {
                const page = pages[i];
                const url = await page.url();
                if (url.includes(varSting1)) {
                  currentPage = page;
                  await currentPage.bringToFront()
                  break;
                }
            }
            let title = await currentPage.title()
            console.log(index, "当前页面：", title)
            // 获取所有具有类名 `.quests_verifyButton__GcXnP` 的元素
            const elements = await currentPage.$$(varSting2);

            // 遍历元素并调用 `click` 方法
            for (let i = 0; i < elements.length; i++) {
                await elements[i].click();
            }
            console.log(index, "click OK!")
            break
        }
        catch(e){
            console.log(index, 'e==>', e.message)
            await sleep(5000)
        }
    }
    
    await sleep(3000)
    await browser.disconnect()
}

if (commandString == "input"){
    console.log(commandString, "...")
    batchInputElement()
}

async function batchInputElement(){
    for(let i = num1; i <= num2; i++){
        let port = portBase + i
        let webSocketDebuggerUrl = "http://127.0.0.1:" + port + "/json/version"
        input(i, port, webSocketDebuggerUrl, varSting1, varSting2, varSting3)
        //await sleep(100)
    }
}


async function input(index, port, webSocketDebuggerUrl, varSting1, varSting2, inputContent) {
    const result = await isPortTaken(port, '127.0.0.1')
    if (result) {
        console.log(index, result, port, "已启动！")
    }
    else {
        return
    }

    let wsKey = await axios.get(webSocketDebuggerUrl);
    let browser = await puppeteer.connect({
        browserWSEndpoint: wsKey.data.webSocketDebuggerUrl,
        defaultViewport:null
    });
    while (true) {
        try{
            const pages = await browser.pages();
            let currentPage
            for (let i = 0; i < pages.length; i++) {
                const page = pages[i];
                const url = await page.url();
                if (url.includes(varSting1)) {
                  currentPage = page;
                  await currentPage.bringToFront()
                  break;
                }
            }
            let title = await currentPage.title()
            console.log(index, "当前页面：", title)
            // 获取所有具有类名 `.quests_verifyButton__GcXnP` 的元素
            const elements = await currentPage.$$(varSting2);

            // 遍历元素并调用 `click` 方法
            for (let i = 0; i < elements.length; i++) {
                await elements[i].type(inputContent);
            }
            console.log(index, "input OK!")
            break
        }
        catch(e){
            console.log(index, 'e==>', e.message)
            await sleep(5000)
        }
    }
    
    //await sleep(3000)
    await browser.disconnect()
}

if (commandString == "close"){
    console.log(commandString, "...")
    batchClosePage()
}

async function batchClosePage(){
    for(let i = num1; i <= num2; i++){
        let port = portBase + i
        let webSocketDebuggerUrl = "http://127.0.0.1:" + port + "/json/version"
        closePage(i, port, webSocketDebuggerUrl, varSting1)
        //await sleep(100)
    }
}


async function closePage(index, port, webSocketDebuggerUrl, toCloseURL) {
    const result = await isPortTaken(port, '127.0.0.1')
    if (result) {
        console.log(index, result, port, "已启动！")
    }
    else {
        return
    }

    let wsKey = await axios.get(webSocketDebuggerUrl);
    let browser = await puppeteer.connect({
        browserWSEndpoint: wsKey.data.webSocketDebuggerUrl,
        defaultViewport:null
    });
    while (true) {
        try{
            const pages = await browser.pages();
            let currentPage
            for (let i = 0; i < pages.length; i++) {
                const page = pages[i];
                const url = await page.url();
                if (url.includes(toCloseURL)) {
                  currentPage = page;
                  await currentPage.close()
                }
            }
            console.log(index, "closePage OK!")
            break
        }
        catch(e){
            console.log(index, 'e==>', e.message)
            await sleep(5000)
        }
    }
    
    //await sleep(3000)
    await browser.disconnect()
}

if (commandString == "signin"){
    console.log(commandString, "...")
    batchSignIn()
}

async function batchSignIn(){
    for(let i = num1; i <= num2; i++){
        let port = portBase + i
        let webSocketDebuggerUrl = "http://127.0.0.1:" + port + "/json/version"
        signIn(i, port, webSocketDebuggerUrl)
        //await sleep(100)
    }
}


async function signIn(index, port, webSocketDebuggerUrl) {
    const result = await isPortTaken(port, '127.0.0.1')
    if (result) {
        console.log(index, result, port, "已启动！")
    }
    else {
        return
    }

    let wsKey = await axios.get(webSocketDebuggerUrl);
    let browser = await puppeteer.connect({
        browserWSEndpoint: wsKey.data.webSocketDebuggerUrl,
        defaultViewport:null
    });
    try{
        const pages = await browser.pages();
        let currentPage = null
        for (let i = 0; i < pages.length; i++) {
            const page = pages[i];
            const url = await page.url();
            if (url.includes("notification")) {
                currentPage = page;
                await currentPage.bringToFront()
                break;
            }
        }
        let title = await currentPage.title()
        console.log(index, "当前页面：", title)
        // 获取所有具有类名 `.quests_verifyButton__GcXnP` 的元素
        const elements = await currentPage.$$("#app-content > div > div > div > div.permissions-connect-choose-account__footer-container > div.page-container__footer > footer > button.button.btn--rounded.btn-primary.page-container__footer-button");

        // 遍历元素并调用 `click` 方法
        for (let i = 0; i < elements.length; i++) {
            await elements[i].click();
        }
        //await currentPage.click('button:contains("Sign-In")');
        console.log(index, "sign in OK!")
    }
    catch(e){
        console.log(index, 'e==>', e.message)
        await sleep(5000)
    }
    
    //await sleep(3000)
    await browser.disconnect()
}


if (commandString == "devmode"){
    console.log(commandString, "...")
    batchSwitchDevmode()
}

async function batchSwitchDevmode(){
    for(let i = num1; i <= num2; i++){
        let port = portBase + i
        let webSocketDebuggerUrl = "http://127.0.0.1:" + port + "/json/version"
        switchDevmode(i, port, webSocketDebuggerUrl)
        //await sleep(100)
    }
}


async function switchDevmode(index, port, webSocketDebuggerUrl) {
    const result = await isPortTaken(port, '127.0.0.1')
    if (result) {
        console.log(index, result, port, "已启动！")
    }
    else {
        return
    }

    let wsKey = await axios.get(webSocketDebuggerUrl);
    let browser = await puppeteer.connect({
        browserWSEndpoint: wsKey.data.webSocketDebuggerUrl,
        defaultViewport:null
    });
    try{
        let page = await browser.newPage()
        const extensionUrl = `chrome://extensions/`;
        await page.goto(extensionUrl, { waitUntil: 'load' });

        const devModeToggle = await page.evaluateHandle(
            'document.querySelector("body > extensions-manager").shadowRoot.querySelector("extensions-toolbar").shadowRoot.querySelector("#devMode")'
          );
          await devModeToggle.click();
        console.log(index, "devMode switch OK!")
    }
    catch(e){
        console.log(index, 'e==>', e.message)
        await sleep(5000)
    }
    
    //await sleep(3000)
    await browser.disconnect()
}


//==================

let token_array = [];
const fs = require('fs').promises;

async function readAndProcessFile() {
  try {
    const data = await fs.readFile('twitter_token.txt', 'utf8');

    // 按行分割内容
    const lines = data.split('\n');

    // 创建一个空数组来保存参数
    let token_array = [];

    // 遍历每行内容
    lines.forEach((line, index) => {
      // 忽略空行
      if (line.trim() === '') {
        return;
      }

      // 按空格分割行内容
      const [num, token] = line.split(' ');

      // 将参数保存到数组中
      token_array.push([num, token])
    });

    token_array = token_array.map(item => [item[0], item[1].replace('\r', '')]);

    console.log(token_array);
  } catch (err) {
    console.error(err);
  }
}

if (commandString == "twlogin"){
    console.log(commandString, "...")
    readAndProcessFile()
    batchTwLogin()
}

async function batchTwLogin(){
    for(let i = num1; i <= num2; i++){
        let port = portBase + i
        let webSocketDebuggerUrl = "http://127.0.0.1:" + port + "/json/version"
        TwLogin(i, port, webSocketDebuggerUrl)
        //await sleep(100)
    }
}

async function TwLogin(index, port, webSocketDebuggerUrl) {
    const result = await isPortTaken(port, '127.0.0.1')
    if (result) {
        console.log(index, result, port, "已启动！")
    }
    else {
        return
    }

    let wsKey = await axios.get(webSocketDebuggerUrl);
    let browser = await puppeteer.connect({
        browserWSEndpoint: wsKey.data.webSocketDebuggerUrl,
        defaultViewport:null
    });
    try{
        let page = await browser.newPage()
        const extensionUrl = "https://twitter.com";
        await page.goto(extensionUrl, { waitUntil: 'load' });
        const auth_token = token_array.find(item => item[0] === index.toString());
        if (auth_token && auth_token.length > 1) {
            await page.evaluate((token) => {
                document.cookie = `auth_token=${token}; Max-Age=30000000; path=/`;
            }, auth_token[1]);
            await page.reload();
            console.log(index, "twitter login OK!")
        } else {
            console.log(index, "auth_token not found")
        }
    }
    catch(e){
        console.log(index, 'e==>', e.message)
        await sleep(5000)
    }
    
    //await sleep(3000)
    await browser.disconnect()
}
//==================
