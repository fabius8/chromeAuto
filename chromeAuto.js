const axios=require('axios');
const puppeteer=require('puppeteer');
const net = require('net');
const path = require('path');
const fs = require('fs');
require("dotenv").config();
const { faker } = require('@faker-js/faker');


const currentDirectory = process.cwd();
const relateDirectory = "pproxy\\switchomega_bak\\"
const metamask_url = "chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html"

let metamask_password = process.env.METAMASK_PASSWORD

//const args = process.argv.slice(2);
const commandString = process.argv[2];
const varSting1 = process.argv[3]
const varSting2 = process.argv[4]
const varSting3 = process.argv[5]
const varSting4 = process.argv[6]
console.log(commandString, varSting1, varSting2, varSting3, varSting4)

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// 读取并验证端口信息
async function getValidPorts() {
    try {
        // 读取 chrome_ports.json
        const portsData = JSON.parse(fs.readFileSync('chrome_ports.json', 'utf8'));
        const validPorts = {};
        let hasChanges = false;

        // 检查每个端口是否可用
        for (const [userNum, port] of Object.entries(portsData)) {
            const isInUse = await isPortTaken(port, '127.0.0.1');
            if (isInUse) {
                validPorts[userNum] = port;
            } else {
                // 如果有端口被移除，标记有变化
                hasChanges = true;
                console.log(`Port ${port} for user ${userNum} is not in use, removing...`);
            }
        }

        // 只在有变化时才写入文件
        if (hasChanges) {
            fs.writeFileSync('chrome_ports.json', JSON.stringify(validPorts, null, 2));
            console.log('Port configuration updated');
        }

        return validPorts;
    } catch (error) {
        console.error('Error reading or processing ports:', error);
        return {};
    }
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

// 通用批处理函数，支持可变参数
async function batchProcess(handler, ...params) {
    const validPorts = await getValidPorts();
    
    // 直接遍历 validPorts 对象
    for (const [userNum, port] of Object.entries(validPorts)) {
        const webSocketDebuggerUrl = `http://127.0.0.1:${port}/json/version`;
        handler(parseInt(userNum), port, webSocketDebuggerUrl, ...params);
    }
}
////////////////////////////////////////////////////////////////////////////////////
//ok wallet YES
if (commandString == "keplrYes"){
    console.log(commandString, "...")
    BatchkeplrYes()
}

// 修改原有的批处理函数
async function BatchkeplrYes(){
    batchProcess(keplrYes, varSting1)
}

async function keplrYes(index, port, webSocketDebuggerUrl, varSting1){
    const result = await isPortTaken(port, '127.0.0.1')
    if (result) {
        console.log(index, result, port, "已启动！")
    }
    else {
        return
    }
    if (varSting1 == null){
        await randomSleep(1, 3 * 1000)
    }else{
        await randomSleep(1, parseInt(varSting1) * 1000)
    }
    let wsKey = await axios.get(webSocketDebuggerUrl);
    let browser = await puppeteer.connect({
        browserWSEndpoint: wsKey.data.webSocketDebuggerUrl,
        defaultViewport:null
    });

    const pages = await browser.pages();
    let currentPage
    for (let i = 0; i < pages.length; i++) {
        const page = pages[i];
        const url = await page.url();
        if (url.includes("dmkamcknogkgcdfhhbddcghachkejeap")) {
            await page.evaluate(() => {
                // 查找包含特定文本的按钮并点击
                const buttons = document.querySelectorAll('button');
                for (const button of buttons) {
                  if (button.textContent.includes('Approve')) {
                    button.click();
                    break;
                  }
                }
            });
        }
    }
    console.log("browser disconnecting...")
    browser.disconnect()
}
////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////
//ok wallet YES
if (commandString == "randomUserName"){
    console.log(commandString, "...")
    batchRandomUsername()
}

// 修改原有的批处理函数
async function batchRandomUsername(){
    batchProcess(randomUsername, varSting1)
}

async function randomUsername(index, port, webSocketDebuggerUrl, varSting1){
    const result = await isPortTaken(port, '127.0.0.1')
    if (result) {
        console.log(index, result, port, "已启动！")
    }
    else {
        return
    }

    await randomSleep(1, 3 * 1000)

    let wsKey = await axios.get(webSocketDebuggerUrl);
    let browser = await puppeteer.connect({
        browserWSEndpoint: wsKey.data.webSocketDebuggerUrl,
        defaultViewport:null
    });

    const pages = await browser.pages();
    let currentPage = null;
    for (const page of pages) {
        const url = await page.url();
        console.log('检查URL:', url); // 调试日志
        if (url.includes(varSting1)) {
            currentPage = page;
            break;
        }
    }
    
    // 直接使用键盘输入随机用户名
    const rawUsername = faker.internet.username();
    // 只保留字母和数字 - 使用更明确的方式
    const username = rawUsername
        .replace(/[._\-]/g, '')  // 特别去除点号、下划线和连字符
        .replace(/[^a-zA-Z0-9]/g, ''); // 再次清除其他所有特殊字符

    console.log(index, currentPage.url(), username)
    //await currentPage.bringToFront(); // 激活当前标签页

    await currentPage.keyboard.type(username);
    //console.log("browser disconnecting...")
    browser.disconnect()
}
////////////////////////////////////////////////////////////////////////////////////
//===========================
if (commandString == "keplrLogin"){
    console.log(commandString, "...")
    BatchKeplrLogin()
}

async function BatchKeplrLogin(){
    batchProcess(keplrLogin, varSting1)
}

async function keplrLogin(index, port, webSocketDebuggerUrl, varSting1){
    const result = await isPortTaken(port, '127.0.0.1')
    if (result) {
        console.log(index, result, port, "已启动！")
    }
    else {
        return
    }
    if (varSting1 == null){
        await randomSleep(1, 3000)
    }else{
        await randomSleep(1, parseInt(varSting1) * 1000)
    }
    let wsKey = await axios.get(webSocketDebuggerUrl);
    let browser = await puppeteer.connect({
        browserWSEndpoint: wsKey.data.webSocketDebuggerUrl,
        defaultViewport:null
    });
    try{
        let page = await browser.newPage()
        const extensionUrl = "chrome-extension://dmkamcknogkgcdfhhbddcghachkejeap/popup.html";
        await page.goto(extensionUrl, { waitUntil: 'load' });
    
        await sleep(100)
        let selector = 'input[type=password]'
        let input = await waitForSelectorWithRetry(page, selector, 2, 2000)
        if (input == null){
            browser.disconnect()
            return
        }
        await input.type(metamask_password);
        await sleep(100)
        await page.keyboard.press('Enter'),

        console.log("第", index, "个", "keplr 已解锁！")
    }catch(e){
        console.log('e==>', e.message)
    }
    console.log("browser disconnecting...")
    browser.disconnect()
}
//===========================
////////////////////////////////////////////////////////////////////////////////////
// keplr autoconfirm sign
if (commandString == "keplrAuto"){
    console.log(commandString, "...")
    BatchKeplrAuto()
}

async function BatchKeplrAuto(){
    batchProcess(keplrAuto, varSting1)
}

async function keplrAuto(index, port, webSocketDebuggerUrl, varSting1){
    const result = await isPortTaken(port, '127.0.0.1')
    if (result) {
        console.log(index, result, port, "已启动！")
    }
    else {
        return
    }
    if (varSting1 == null){
        await randomSleep(1, 3 * 1000)
    }else{
        await randomSleep(1, parseInt(varSting1) * 1000)
    }
    let wsKey = await axios.get(webSocketDebuggerUrl);
    let browser = await puppeteer.connect({
        browserWSEndpoint: wsKey.data.webSocketDebuggerUrl,
        defaultViewport:null
    });
    await keplrMonitorElement(index, browser);
}

async function keplrMonitorElement(index, browser) {
    browser.on('targetcreated', async target => {
        if (target.type() === 'page') {
            const newPage = await target.page();
            try{
                await newPage.waitForNavigation({ timeout: 8000 }); // 等待新页面加载完成
            }catch(e){
                console.log(index, "页面导航超时:", e.message)
            }
            const url = newPage.url()
            console.log('新页面已加载完毕:', url);

            if (url.includes("dmkamcknogkgcdfhhbddcghachkejeap")) {
                try {
                    const Button = 'button.sc-jOrMOR.jYRHFp'; // 你想监控的元素的选择器
                    await newPage.waitForSelector(Button, { visible: true, timeout: 3000 });
                    await newPage.click(Button);
                    console.log(index, "点击成功！");
                    // const buttons = await newPage.evaluate(() => {
                    //     const buttons = Array.from(document.querySelectorAll('button'));
                    //     return buttons.map(button => button.textContent);
                    // });
                    // console.log('Buttons:', buttons);

                    // await newPage.evaluate(() => {
                    //     const buttons = document.querySelectorAll('button');
                    //     for (const button of buttons) {
                    //         if (button.textContent.includes('Approve')) {
                    //             button.click();
                    //             break;
                    //         }
                    //     }
                    // });
                } catch (error) {
                    console.error(index, `出现错误: ${error}`);
                    await sleep(3000);
                }
            }
        }
        // 在这里可以对新页面进行操作
    });
}
////////////////////////////////////////////////////////////////////////////////////
//===========================
if (commandString == "initiaLogin"){
    console.log(commandString, "...")
    BatchInitiaLogin()
}

async function BatchInitiaLogin(){
    batchProcess(initiaLogin, varSting1)
}

async function initiaLogin(index, port, webSocketDebuggerUrl, varSting1){
    const result = await isPortTaken(port, '127.0.0.1')
    if (result) {
        console.log(index, result, port, "已启动！")
    }
    else {
        return
    }
    if (varSting1 == null){
        await randomSleep(1, 3000)
    }else{
        await randomSleep(1, parseInt(varSting1) * 1000)
    }
    let wsKey = await axios.get(webSocketDebuggerUrl);
    let browser = await puppeteer.connect({
        browserWSEndpoint: wsKey.data.webSocketDebuggerUrl,
        defaultViewport:null
    });
    try{
        let page = await browser.newPage()
        const extensionUrl = "chrome-extension://ffbceckpkpbcmgiaehlloocglmijnpmp/index.html";
        await page.goto(extensionUrl, { waitUntil: 'load' });
    
        await sleep(100)
        let selector = 'input[type=password]'
        let input = await waitForSelectorWithRetry(page, selector, 2, 2000)
        if (input == null){
            browser.disconnect()
            return
        }
        await input.type(metamask_password);
        await sleep(100)
        await page.keyboard.press('Enter'),

        console.log("第", index, "个", "keplr 已解锁！")
    }catch(e){
        console.log('e==>', e.message)
    }
    console.log("browser disconnecting...")
    browser.disconnect()
}
//===========================
////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////
if (commandString == "initiaAuto"){
    console.log(commandString, "...")
    BatchInitiaAuto()
}

async function BatchInitiaAuto(){
    batchProcess(initiaAuto, varSting1)
}

async function initiaAuto(index, port, webSocketDebuggerUrl, varSting1){
    const result = await isPortTaken(port, '127.0.0.1')
    if (result) {
        console.log(index, result, port, "已启动！")
    }
    else {
        return
    }
    if (varSting1 == null){
        await randomSleep(1, 3 * 1000)
    }else{
        await randomSleep(1, parseInt(varSting1) * 1000)
    }
    let wsKey = await axios.get(webSocketDebuggerUrl);
    let browser = await puppeteer.connect({
        browserWSEndpoint: wsKey.data.webSocketDebuggerUrl,
        defaultViewport:null
    });
    await initiaMonitorElement(index, browser);
}

async function initiaMonitorElement(index, browser) {
    browser.on('targetcreated', async target => {
        if (target.type() === 'page') {
            const newPage = await target.page();
            try{
                await newPage.waitForNavigation({ timeout: 8000 }); // 等待新页面加载完成
            }catch(e){
                console.log(index, "页面导航超时:", e.message)
            }
            const url = newPage.url()
            console.log('新页面已加载完毕:', url);

            if (url.includes("ffbceckpkpbcmgiaehlloocglmijnpmp")) {
                try {
                    const Button = 'button[type="submit"]'; // 你想监控的元素的选择器
                    await newPage.waitForSelector(Button, { visible: true, timeout: 3000 });
                    await newPage.click(Button);
                    console.log(index, "点击成功！");

                } catch (error) {
                    console.error(index, `出现错误: ${error}`);
                    await sleep(3000);
                }
            }
        }
        // 在这里可以对新页面进行操作
    });
}
////////////////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////////////////
//===========================
if (commandString == "tgQueryId"){
    console.log(commandString, "...")
    BatchTgQueryId()
}

async function BatchTgQueryId(){
    batchProcess(TgQueryId, varSting1)
}

async function TgQueryId(index, port, webSocketDebuggerUrl, varSting1){
    const result = await isPortTaken(port, '127.0.0.1')
    if (result) {
        console.log(index, result, port, "已启动！")
    }
    else {
        return
    }
    if (varSting1 == null){
        await randomSleep(1, 3000)
    }else{
        await randomSleep(1, parseInt(varSting1) * 1000)
    }
    let wsKey = await axios.get(webSocketDebuggerUrl);
    let browser = await puppeteer.connect({
        browserWSEndpoint: wsKey.data.webSocketDebuggerUrl,
        defaultViewport:null
    });
    try{
        const pages = await browser.pages();
        const page = pages.find(page => page.url().includes('web.telegram.org'));

        // 获取所有frame的sessionStorage
        const allFramesData = await page.evaluate(async () => {
            const getAllStorageData = (frame) => {
                try {
                    const data = {};
                    Object.keys(frame.sessionStorage).forEach(key => {
                        data[key] = frame.sessionStorage.getItem(key);
                    });
                    return data;
                } catch (e) {
                    return null;  // 如果无法访问则返回null
                }
            };

            // 获取主frame的数据
            const result = {
                mainFrame: {
                    url: window.location.href,
                    sessionStorage: getAllStorageData(window)
                },
                frames: []
            };

            // 获取所有iframe的数据
            const iframes = document.querySelectorAll('iframe');
            for (const iframe of iframes) {
                try {
                    const frameData = {
                        url: iframe.src,
                        sessionStorage: getAllStorageData(iframe.contentWindow)
                    };
                    result.frames.push(frameData);
                } catch (e) {
                    console.error('无法访问iframe:', iframe.src);
                }
            }

            return result;
        });
        const url = allFramesData.frames[0].url;
        const searchParams = new URL(url).hash.substring(1); // 去掉 # 号
        const params = new URLSearchParams(searchParams);
        const tgWebAppData = params.get('tgWebAppData');
        const decodedData = decodeURIComponent(tgWebAppData);
        
        // 解析 tgWebAppData 中的参数
        const tgParams = new URLSearchParams(decodedData);
        const queryId = tgParams.get('query_id');
        const userData = JSON.parse(tgParams.get('user'));
        //console.log('user:', userData);
        console.log(index, " ", tgWebAppData);


    }catch(e){
        console.log('e==>', e.message)
    }
    console.log("browser disconnecting...")
    browser.disconnect()

}











//===========================
////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////
if (commandString == "metamaskLogin"){
    console.log(commandString, "...")
    BatchMetamaskLogin()
}

async function BatchMetamaskLogin(){
    batchProcess(metamaskLogin, varSting1)
}

async function metamaskLogin(index, port, webSocketDebuggerUrl, varSting1){
    const result = await isPortTaken(port, '127.0.0.1')
    if (result) {
        console.log(index, result, port, "已启动！")
    }
    else {
        return
    }
    if (varSting1 == null){
        await randomSleep(1, 3000)
    }else{
        await randomSleep(1, parseInt(varSting1) * 1000)
    }
    let wsKey = await axios.get(webSocketDebuggerUrl);
    let browser = await puppeteer.connect({
        browserWSEndpoint: wsKey.data.webSocketDebuggerUrl,
        defaultViewport:null
    });
    try{
        let page = await browser.newPage()
        const extensionUrl = metamask_url;
        await page.goto(extensionUrl, { waitUntil: 'load' });
    
        await sleep(100)
        let selector = 'input[id=password]'
        let input = await waitForSelectorWithRetry(page, selector, 2, 2000)
        if (input == null){
            browser.disconnect()
            return
        }
        await input.type(metamask_password);
        await sleep(100)
        await page.keyboard.press('Enter'),

        console.log("第", index, "个", "metamask 已解锁！")
    }catch(e){
        console.log('e==>', e.message)
    }
    console.log("browser disconnecting...")
    browser.disconnect()
}
//===========================
if (commandString == "okLogin"){
    console.log(commandString, "...")
    BatchOkLogin()
}

async function BatchOkLogin(){
    batchProcess(okLogin, varSting1)
}

async function okLogin(index, port, webSocketDebuggerUrl, varSting1){
    const result = await isPortTaken(port, '127.0.0.1')
    if (result) {
        console.log(index, result, port, "已启动！")
    }
    else {
        return
    }
    if (varSting1 == null){
        await randomSleep(1, 3000)
    }else{
        await randomSleep(1, parseInt(varSting1) * 1000)
    }
    let wsKey = await axios.get(webSocketDebuggerUrl);
    let browser = await puppeteer.connect({
        browserWSEndpoint: wsKey.data.webSocketDebuggerUrl,
        defaultViewport:null
    });
    try{
        let page = await browser.newPage()
        const extensionUrl = "chrome-extension://mcohilncbfahbmgdjkbpemcciiolgcge/popup.html";
        await page.goto(extensionUrl, { waitUntil: 'load' });
    
        await sleep(100)
        let selector = 'input[type="password"]'
        let input = await waitForSelectorWithRetry(page, selector, 2, 2000)
        if (input == null){
            browser.disconnect()
            return
        }
        await input.type(metamask_password);
        await sleep(100)
        await page.keyboard.press('Enter'),
        await sleep(100)
        console.log("第", index, "个", "okx 已解锁！")
        await page.close()
    }catch(e){
        console.log('e==>', e.message)
    }
    console.log("browser disconnecting...")
    browser.disconnect()
}
//===========================
if (commandString == "enableWallet"){
    console.log(commandString, "...")
    BatchEnableWallet()
}

async function BatchEnableWallet(){
    batchProcess(enableWallet, varSting1, varSting2)
}

async function enableWallet(index, port, webSocketDebuggerUrl, varSting1, varSting2){
    let enableWalletID = ""
    const metamaskID = "nkbihfbeogaeaoehlefnkodbefgpgknn"
    const okxID = "mcohilncbfahbmgdjkbpemcciiolgcge"
    if(varSting1.includes("metamask")){
        enableWalletID = metamaskID
    }
    if(varSting1.includes("okx")){
        enableWalletID = okxID
    }
    const result = await isPortTaken(port, '127.0.0.1')
    if (result) {
        console.log(index, result, port, "已启动！")
    }
    else {
        return
    }
    if (varSting2 == null){
        await randomSleep(1, 3000)
    }else{
        await randomSleep(1, parseInt(varSting2) * 1000)
    }
    let wsKey = await axios.get(webSocketDebuggerUrl);
    let browser = await puppeteer.connect({
        browserWSEndpoint: wsKey.data.webSocketDebuggerUrl,
        defaultViewport:null
    });
    try{
        const page = await browser.newPage(); // 打开新页面
        await page.goto(`chrome://extensions/?id=${enableWalletID}`); // 导航到目标页面
        const enableToggle = await page.evaluate(() => {
            const status = document.querySelector("body > extensions-manager").shadowRoot.querySelector("#viewManager > extensions-detail-view").shadowRoot.querySelector("#enableToggle").ariaPressed
            if(status == 'false'){
                document.querySelector("body > extensions-manager").shadowRoot.querySelector("#viewManager > extensions-detail-view").shadowRoot.querySelector("#enableToggle").click()
            }
            return status;
        });
        await sleep(100)
        await page.close()
    }catch(e){
        console.log('e==>', e.message)
    }
    console.log("browser disconnecting...")
    browser.disconnect()
}
//===========================
if (commandString == "disenableWallet"){
    console.log(commandString, "...")
    BatchDisenableWallet()
}

async function BatchDisenableWallet(){
    batchProcess(disenableWallet, varSting1, varSting2)
}

async function disenableWallet(index, port, webSocketDebuggerUrl, varSting1, varSting2){
    let disenableWalletID = ""
    const metamaskID = "nkbihfbeogaeaoehlefnkodbefgpgknn"
    const okxID = "mcohilncbfahbmgdjkbpemcciiolgcge"
    if(varSting1.includes("metamask")){
        disenableWalletID = metamaskID
    }
    if(varSting1.includes("okx")){
        disenableWalletID = okxID
    }
    const result = await isPortTaken(port, '127.0.0.1')
    if (result) {
        console.log(index, result, port, "已启动！")
    }
    else {
        return
    }
    if (varSting2 == null){
        await randomSleep(1, 3000)
    }else{
        await randomSleep(1, parseInt(varSting2) * 1000)
    }
    let wsKey = await axios.get(webSocketDebuggerUrl);
    let browser = await puppeteer.connect({
        browserWSEndpoint: wsKey.data.webSocketDebuggerUrl,
        defaultViewport:null
    });
    try{
        const page = await browser.newPage(); // 打开新页面
        await page.goto(`chrome://extensions/?id=${disenableWalletID}`); // 导航到目标页面
        const enableToggle = await page.evaluate(() => {
            const status = document.querySelector("body > extensions-manager").shadowRoot.querySelector("#viewManager > extensions-detail-view").shadowRoot.querySelector("#enableToggle").ariaPressed
            if(status == 'true'){
                document.querySelector("body > extensions-manager").shadowRoot.querySelector("#viewManager > extensions-detail-view").shadowRoot.querySelector("#enableToggle").click()
            }
            return status;
        });
        await sleep(100)
        await page.close()
    }catch(e){
        console.log('e==>', e.message)
    }
    console.log("browser disconnecting...")
    browser.disconnect()
}
//===========================

async function waitForSelectorWithRetry(page, selector, maxRetries = 2, retryInterval = 1000) {
    let retries = 0;
    let input = null
    while (retries < maxRetries) {
      try {
        input = await page.waitForSelector(selector, { timeout: 5000 });
        //console.log('Element found!');
        return input
      } catch (error) {
        // 如果超时或找不到元素，继续重试
        console.log(`${selector} not found. Retrying... (Attempt ${retries + 1}/${maxRetries})`);
        retries++;
        await new Promise(resolve => setTimeout(resolve, retryInterval)); // 等待一段时间后重试
      }
    }
    
    console.log(`Maximum retries reached. ${selector} not found.`);
    return null
}
////////////////////////////////////////////////////////////////////////////////////
//ok wallet YES
if (commandString == "okYes"){
    console.log(commandString, "...")
    BatchOkYes()
}

async function BatchOkYes(){
    batchProcess(okYes, varSting1)
}

async function okYes(index, port, webSocketDebuggerUrl, varSting1){
    const result = await isPortTaken(port, '127.0.0.1')
    if (result) {
        console.log(index, result, port, "已启动！")
    }
    else {
        return
    }
    if (varSting1 == null){
        await randomSleep(1, 3 * 1000)
    }else{
        await randomSleep(1, parseInt(varSting1) * 1000)
    }
    let wsKey = await axios.get(webSocketDebuggerUrl);
    let browser = await puppeteer.connect({
        browserWSEndpoint: wsKey.data.webSocketDebuggerUrl,
        defaultViewport:null
    });

    const pages = await browser.pages();
    let currentPage
    for (let i = 0; i < pages.length; i++) {
        const page = pages[i];
        const url = await page.url();
        if (url.includes("notification") && (url.includes("mcohilncbfahbmgdjkbpemcciiolgcge"))) {
            currentPage = page;
            let title = await currentPage.title()
            console.log(index, "当前页面：", title)
            const Button = 'button[class="okui-btn btn-lg btn-fill-highlight mobile _action-button_j3bvq_1"]'; // 你想监控的元素的选择器
            await currentPage.waitForSelector(Button, { visible: true, timeout: 3000 });
            await currentPage.click(Button);
            console.log(index, "点击成功！");
            break;
        }
    }
    console.log("browser disconnecting...")
    browser.disconnect()
}
////////////////////////////////////////////////////////////////////////////////////
// ok autoconfirm sign
if (commandString == "okAuto"){
    console.log(commandString, "...")
    BatchOkAuto()
}

async function BatchOkAuto(){
    batchProcess(okAuto, varSting1)
}

async function okAuto(index, port, webSocketDebuggerUrl, varSting1){
    const result = await isPortTaken(port, '127.0.0.1')
    if (result) {
        console.log(index, result, port, "已启动！")
    }
    else {
        return
    }
    if (varSting1 == null){
        await randomSleep(1, 3 * 1000)
    }else{
        await randomSleep(1, parseInt(varSting1) * 1000)
    }
    let wsKey = await axios.get(webSocketDebuggerUrl);
    let browser = await puppeteer.connect({
        browserWSEndpoint: wsKey.data.webSocketDebuggerUrl,
        defaultViewport:null
    });
    await okMonitorElement(index, browser);
}

async function okMonitorElement(index, browser) {
    browser.on('targetcreated', async target => {
        if (target.type() === 'page') {
            const newPage = await target.page();
            try{
                await newPage.waitForNavigation({ timeout: 5000 }); // 等待新页面加载完成
            }catch(e){
                console.log(index, "页面导航超时:", e.message)
            }
            const url = newPage.url()
            console.log('新页面已加载完毕:', url);

            if (url.includes("notification") && (url.includes("mcohilncbfahbmgdjkbpemcciiolgcge"))) {
                const selectors = [
                    '.page-container.permissions-connect', // 链接
                    '._root_1wel2_1', // 签名
                    '.app-content.os-win.browser-chrome',
                ];
                
                const promises = selectors.map(selector =>
                    newPage.waitForSelector(selector, { timeout: 3000 }).then(() => selector).catch(() => null)
                );
                
                try {
                    let unfindCount = 0
                    while (!newPage.isClosed()) {
                        const matchedSelector = await Promise.race(promises.filter(p => p)); // 过滤掉为 null 的 Promise
                        if (matchedSelector) {
                            console.log(`匹配的选择器为: ${matchedSelector}`);
                            const matchedIndex = selectors.indexOf(matchedSelector);
                            console.log("序号：", matchedIndex);
                            // 签名
                            if((matchedIndex == 0 || matchedIndex == 1 || matchedIndex == 2)){
                                const Button = 'button[class="okui-btn btn-lg btn-fill-highlight mobile _action-button_j3bvq_1"]'; // 你想监控的元素的选择器
                                await newPage.waitForSelector(Button, { visible: true, timeout: 8000 });
                                await newPage.click(Button);
                                console.log(index, "点击成功！");
                                await sleep(3000)
                            }else if(matchedIndex == 3){
                                await newPage.click(matchedSelector);
                                console.log(index, "切换网络成功！");
                                await sleep(3000)
                            }else if(matchedIndex == 1){ // ❌付款，这里跳出循环
                                console.log(index, "付款页面，不处理！")
                                break
                            }else if(matchedIndex == 1){ // ❌授权，这里跳出循环
                                console.log(index, "授权页面，不处理！")
                                break
                            }
                        } else {
                            console.error(index, `无法找到任何选择器或超时`);
                            await sleep(3000)
                            if (unfindCount < 3){
                                unfindCount = unfindCount + 1 
                            }else{
                                break
                            }
                        }
                    }
                } catch (error) {
                    console.error(index, `出现错误: ${error}`);
                    await sleep(3000)
                }
            }
        }
        // 在这里可以对新页面进行操作
    });
}



////////////////////////////////////////////////////////////////////////////////////
// metamask autoconfirm sign
if (commandString == "mmAuto"){
    console.log(commandString, "...")
    BatchMetamaskAutoSign()
}

async function BatchMetamaskAutoSign(){
    batchProcess(metamaskAutoSign, varSting1)
}

async function metamaskAutoSign(index, port, webSocketDebuggerUrl, varSting1){
    const result = await isPortTaken(port, '127.0.0.1')
    if (result) {
        console.log(index, result, port, "已启动！")
    }
    else {
        return
    }
    if (varSting1 == null){
        await randomSleep(1, 3 * 1000)
    }else{
        await randomSleep(1, parseInt(varSting1) * 1000)
    }
    let wsKey = await axios.get(webSocketDebuggerUrl);
    let browser = await puppeteer.connect({
        browserWSEndpoint: wsKey.data.webSocketDebuggerUrl,
        defaultViewport:null
    });
    await monitorElement(index, browser);
}

async function monitorElement(index, browser) {
    browser.on('targetcreated', async target => {
        if (target.type() === 'page') {
            const newPage = await target.page();
            try{
                await newPage.waitForNavigation({ timeout: 10000 }); // 等待新页面加载完成
            }catch(e){
                console.log(index, "页面导航超时:", e.message)
            }
            const url = newPage.url()
            console.log('新页面已加载完毕:', url);

            if (url.includes("notification")) {
                const selectors = [
                    '.request-signature__navigation', // 签名 page-container-footer-next
                    '.choose-account-list', // 下一步 page-container-footer-next
                    '.permission-approval-container__content', //连接 page-container-footer-next
                    'button[data-testid="confirmation-submit-button"]',  // 可能网络
                    '.confirm-page-container-content', // 确认付款
                    '.box.token-allowance-container.page-container.box--flex-direction-row'  // 授权金额
                ];
                
                const promises = selectors.map(selector =>
                    newPage.waitForSelector(selector, { timeout: 5000 }).then(() => selector).catch(() => null)
                );
                
                try {
                    let unfindCount = 0
                    while (!newPage.isClosed()) {
                        const matchedSelector = await Promise.race(promises.filter(p => p)); // 过滤掉为 null 的 Promise
                        if (matchedSelector) {
                            console.log(`匹配的选择器为: ${matchedSelector}`);
                            const matchedIndex = selectors.indexOf(matchedSelector);
                            console.log("序号：", matchedIndex);
                            // 签名
                            if((matchedIndex == 0) || (matchedIndex == 1) || (matchedIndex == 2)){
                                const Button = 'button[data-testid="page-container-footer-next"]'; // 你想监控的元素的选择器
                                await newPage.waitForSelector(Button, { visible: true, timeout: 3000 });
                                await newPage.click(Button);
                                console.log(index, "点击成功！");
                                await sleep(3000)
                            }else if(matchedIndex == 3){
                                await newPage.click(matchedSelector);
                                console.log(index, "切换网络成功！");
                                await sleep(3000)
                            }else if(matchedIndex == 4){ // ❌付款，这里跳出循环
                                console.log(index, "付款页面，不处理！")
                                break
                            }else if(matchedIndex == 5){ // ❌授权，这里跳出循环
                                console.log(index, "授权页面，不处理！")
                                break
                            }
                        } else {
                            console.error(index, `无法找到任何选择器或超时`);
                            await sleep(3000)
                            if (unfindCount < 3){
                                unfindCount = unfindCount + 1 
                            }else{
                                break
                            }
                        }
                    }
                } catch (error) {
                    console.error(index, `出现错误: ${error}`);
                    await sleep(3000)
                }
            }
        }
        // 在这里可以对新页面进行操作
    });
}


// async function monitorElement(page, buttonXPath) {
//     const checkElement = async () => {
//         await page.reload({ waitUntil: "networkidle0" });
//         console.log("aaaa")

//         const buttons = await page.$x(buttonXPath);
//         console.log("cccc")
//         if (buttons.length > 0) {
//             console.log(`Element found on ${page.url()}`);
//             console.log("bbbb")
//             await buttons[0].click();
//         } else {
//             console.log(`Element not found on ${page.url()}, retrying...`);
//             // 等待一段时间后再次检查
//             setTimeout(checkElement, 5000); // 例如，每隔1秒检查一次
//         }
//     };
//     checkElement();
// }

////////////////////////////////////////////////////////////////////////////////////

// 命令处理
if (commandString == "proxyLoad"){
    console.log(commandString, "...")
    BatchProxyConfigLoad()
}

async function BatchProxyConfigLoad(){
    batchProcess(proxyConfigLoad)
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
    batchProcess(openURL, varSting1, varSting2, varSting3)
}
//varSting3 close time
async function openURL(index, port, webSocketDebuggerUrl, varSting1, varSting2, varSting3){
    const result = await isPortTaken(port, '127.0.0.1')
    if (result) {
        console.log(index, result, port, "已启动！")
    }
    else {
        return
    }
    if (varSting2 == null){
        await randomSleep(1, 5000)
    }else{
        await randomSleep(1, parseInt(varSting2) * 1000)
    }
    let browser = null
    let page = null
    try{
        let wsKey = await axios.get(webSocketDebuggerUrl);
        browser = await puppeteer.connect({
            browserWSEndpoint: wsKey.data.webSocketDebuggerUrl,
            defaultViewport:null,
        });

        page = await browser.newPage()
    
        //await page.goto(varSting1, { waitUntil: 'load' });
        await page.goto(varSting1);
        console.log(index, '网页打开成功！', varSting1);
        //await sleep(3000)
        if (varSting3){
            await sleep(parseInt(varSting3) * 1000)
            await page.close()
        }
    } catch (e) {
        console.log(e.message);
    } finally {
        if (browser) {
            browser.disconnect();
        }
    }
}

//==========================================
if (commandString == "galxeTwMission"){
    console.log(commandString, "...")
    batchGalxeTwMission()
}

async function batchGalxeTwMission(){
    batchProcess(galxeTwMission, varSting1, varSting2, varSting3)
}

//varSting3 close time
async function galxeTwMission(index, port, webSocketDebuggerUrl, varSting1, varSting2, varSting3){
    const result = await isPortTaken(port, '127.0.0.1')
    if (result) {
        console.log(index, result, port, "已启动！")
    }
    else {
        return
    }
    if (varSting2 == null){
        await randomSleep(1, 5000)
    }else{
        await randomSleep(1, parseInt(varSting2) * 1000)
    }
    let browser = null
    let page = null
    try{
        let wsKey = await axios.get(webSocketDebuggerUrl);
        browser = await puppeteer.connect({
            browserWSEndpoint: wsKey.data.webSocketDebuggerUrl,
            defaultViewport:null,
        });

        const pages = await browser.pages();
        let currentPage
        for (let i = 0; i < pages.length; i++) {
            const page = pages[i];
            const url = await page.url();
            if (url.includes("galxe")) {
              currentPage = page;
              await currentPage.bringToFront()
              break;
            }
        }
        let title = await currentPage.title()
        console.log(index, "当前页面：", title)
        
        const elementsToClick = await currentPage.$$eval('.d-flex.height-100.width-100.click-area', elements => {
            elements.forEach(element => {
              const event = new MouseEvent('click', {
                view: window,
                bubbles: true,
                cancelable: true
              });
              element.dispatchEvent(event);
            });
          });
        
    } catch (e) {
        console.log(e.message);
    } finally {
        if (browser) {
            browser.disconnect();
        }
    }
}

//==========================================



if (commandString == "argentLogin"){
    console.log(commandString, "...")
    argent()
}

async function argent(){
    batchProcess(argentLogin)
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
    batchProcess(click, varSting1, varSting2)
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
    batchProcess(input, varSting1, varSting2, varSting3)
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
    batchProcess(closePage, varSting1)
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
    console.log("browser disconnecting...")
    browser.disconnect()
}

if (commandString == "signin"){
    console.log(commandString, "...")
    batchSignIn()
}

async function batchSignIn(){
    batchProcess(signIn)
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
    batchProcess(switchDevmode)
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


//================== TW

let token_array = [];
//const fs = require('fs').promises;

async function readAndProcessFileTwitter() {
  try {
    const data = await fs.readFile('twitter_token.txt', 'utf8');

    // 按行分割内容
    const lines = data.split('\n');

    // 创建一个空数组来保存参数

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
    readAndProcessFileTwitter()
    batchTwLogin()
}

async function batchTwLogin(){
    batchProcess(TwLogin)
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
            console.log(index, auth_token[1], "twitter login OK!")
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

//================== discord

let discord_token_array = [];

async function readAndProcessFileDiscord() {
  try {
    const data = await fs.readFile('discord_token.txt', 'utf8');

    // 按行分割内容
    const lines = data.split('\n');

    // 创建一个空数组来保存参数

    // 遍历每行内容
    lines.forEach((line, index) => {
      // 忽略空行
      if (line.trim() === '') {
        return;
      }

      // 按空格分割行内容
      const [num, token] = line.split(' ');

      // 将参数保存到数组中
      discord_token_array.push([num, token])
    });

    discord_token_array = discord_token_array.map(item => [item[0], item[1].replace('\r', '')]);

    //console.log(discord_token_array);
  } catch (err) {
    console.error(err);
  }
}

if (commandString == "dislogin"){
    console.log(commandString, "...")
    readAndProcessFileDiscord()
    batchDiscordLogin()
}

async function batchDiscordLogin(){
    batchProcess(discordLogin)
}

async function discordLogin(index, port, webSocketDebuggerUrl) {
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
        const auth_token = discord_token_array.find(item => item[0] === index.toString());
        
        if (auth_token && auth_token.length > 1) {
            let page = await browser.newPage()
            const extensionUrl = "https://discord.com/login";
            await page.goto(extensionUrl, { waitUntil: 'load' });
            await page.evaluate((token) => {
                document.body.appendChild(document.createElement('iframe')).contentWindow.localStorage.token = `"${token}"`;
            }, auth_token[1]);
            await page.reload();
            console.log(index, "discord login OK!")
        } else {
            console.log(index, "auth_token not found")
        }
    }
    catch(e){
        console.log(index, 'e==>', e.message)
        //await sleep(5000)
    }
    
    //await sleep(3000)
    browser.disconnect()
}
//==================
if (commandString == "clickNiu"){
    console.log(commandString, "...")
    batchClickNiu()
}

async function batchClickNiu(){
    batchProcess(clickNiu)
}

async function clickNiu(index, port, webSocketDebuggerUrl) {
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
        // 获取所有页面
        const pages = await browser.pages();
        let targetPage = null;

        // 查找目标页面
        for (const page of pages) {
            const url = await page.url();
            if (url.includes('tap.eclipse.xyz')) {
                console.log('找到页面', page.url());
                targetPage = page;
                break;
            }
        }

        if (!targetPage) {
            console.log('未找到目标页面');
            await browser.close();
            return;
        }

        // 确保canvas元素存在
        const canvasExists = await targetPage.evaluate(() => {
            return !!document.querySelector('canvas');
        }).catch(() => false);

        if (!canvasExists) {
            console.log('Canvas元素不存在，停止点击');
            return;
        }
        console.log('找到Canvas元素', canvasExists);

        try {
            // 获取 canvas 元素的位置和尺寸
            const canvasRect = await targetPage.evaluate(() => {
                const canvas = document.querySelector('canvas');
                const rect = canvas.getBoundingClientRect();
                return {
                    x: rect.left,
                    y: rect.top,
                    width: canvas.width,
                    height: canvas.height
                };
            });
            for (let i = 0; i < 10; i++) {
                // 生成随机点击位置
                const clickX = canvasRect.x + Math.random() * canvasRect.width;
                const clickY = canvasRect.y + Math.random() * canvasRect.height;

                // 执行点击
                await targetPage.mouse.click(clickX, clickY);

                // 生成随机延迟（1-2.5秒）
                const delay = 1000 + Math.random() * 1500;
                await sleep(delay)
            }
            
        } catch (error) {
            console.error('点击过程出错:', error);
            await browser.close();
        }
    }
    catch(e){
        console.log(index, 'e==>', e.message)
        await sleep(5000)
    }
    
    //await sleep(3000)
    console.log(index, "点击结束")
    await browser.disconnect()
}
//==================
////////////////////////////////////////////////////////////////////////////////////
//===========================
if (commandString == "phantomLogin"){
    console.log(commandString, "...")
    batchPhantomLogin()
}

async function batchPhantomLogin(){
    batchProcess(phantomLogin, varSting1)
}

async function phantomLogin(index, port, webSocketDebuggerUrl, varSting1){
    const result = await isPortTaken(port, '127.0.0.1')
    if (result) {
        console.log(index, result, port, "已启动！")
    }
    else {
        return
    }
    if (varSting1 == null){
        await randomSleep(1, 3000)
    }else{
        await randomSleep(1, parseInt(varSting1) * 1000)
    }
    let wsKey = await axios.get(webSocketDebuggerUrl);
    let browser = await puppeteer.connect({
        browserWSEndpoint: wsKey.data.webSocketDebuggerUrl,
        defaultViewport:null
    });
    try{
        let page = await browser.newPage()
        const extensionUrl = "chrome-extension://bfnaelmomeimhlpmgjnjophhpkkoljpa/popup.html";
        await page.goto(extensionUrl, { waitUntil: 'load' });
    
        await sleep(100)
        let selector = 'input[type=password]'
        let input = await waitForSelectorWithRetry(page, selector, 2, 2000)
        if (input == null){
            browser.disconnect()
            return
        }
        await input.type(metamask_password);
        await sleep(100)
        await page.keyboard.press('Enter'),

        console.log("第", index, "个", "keplr 已解锁！")
    }catch(e){
        console.log('e==>', e.message)
    }
    console.log("browser disconnecting...")
    browser.disconnect()
}
//===========================
////////////////////////////////////////////////////////////////////////////////////
//===========================
if (commandString == "backpackLogin"){
    console.log(commandString, "...")
    batchBackpackLogin()
}

async function batchBackpackLogin(){
    batchProcess(backpackLogin, varSting1)
}

async function backpackLogin(index, port, webSocketDebuggerUrl, varSting1){
    const result = await isPortTaken(port, '127.0.0.1')
    if (result) {
        console.log(index, result, port, "已启动！")
    }
    else {
        return
    }
    if (varSting1 == null){
        await randomSleep(1, 3000)
    }else{
        await randomSleep(1, parseInt(varSting1) * 1000)
    }
    let wsKey = await axios.get(webSocketDebuggerUrl);
    let browser = await puppeteer.connect({
        browserWSEndpoint: wsKey.data.webSocketDebuggerUrl,
        defaultViewport:null
    });
    try{
        let page = await browser.newPage()
        const extensionUrl = "chrome-extension://aflkmfhebedbjioipglgcbcmnbpgliof/popup.html";
        await page.goto(extensionUrl, { waitUntil: 'load' });
    
        await sleep(100)
        let selector = 'input[type=password]'
        let input = await waitForSelectorWithRetry(page, selector, 2, 2000)
        if (input == null){
            browser.disconnect()
            return
        }
        await input.type(metamask_password);
        await sleep(100)
        await page.keyboard.press('Enter'),

        console.log("第", index, "个", "keplr 已解锁！")
    }catch(e){
        console.log('e==>', e.message)
    }
    console.log("browser disconnecting...")
    browser.disconnect()
}
//===========================