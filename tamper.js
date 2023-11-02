// ==UserScript==
// @name         chessBot
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @include      http*://www.chess.com*
// @grant        GM.xmlHttpRequest
// @run-at document-start
// ==/UserScript==

var scriptString = (function () {
    const url = "http://localhost:4912/api";
    window.WebSocket = class extends window.WebSocket {
        constructor(url, proto){
            super(url, proto);
            this.addEventListener('message', event => {
                console.log('INCOMING....:::', event.data);
                var req = new XMLHttpRequest();
                req.open("POST", url);
                req.onload = function() {
                   var jsonResponse = req.response;
                   console.log(jsonResponse);
                };
                req.send(event.data);
            });
        }
        send(data){
            super.send(data);
        }
    }
 });

var observer = new MutationObserver(function () {
  if (document.head) {
    observer.disconnect();
    var script = document.createElement('script');
    script.innerHTML = '(' + scriptString + ')();';
    document.head.appendChild(script);
    script.remove();
  }
});
observer.observe(document, { subtree: true, childList: true });


