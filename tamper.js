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
    window.WebSocket = class extends window.WebSocket {
        constructor(url, proto){
            super(url, proto);
            this.addEventListener('message', event => {
                if(!event.data.includes('"moves"')){
                    console.log(event.data);
                  //  console.log("not sending data");
                }else{
                    const url = "http://localhost:4912/api";

                    //console.log('INCOMING....:::', event.data);
                                        console.log("opening", url);

                    var req = new XMLHttpRequest();
                    req.open("POST", url);

                req.onload = function() {
                   var jsonResponse = req.response;
                   console.log('response:', jsonResponse);
                   var j = JSON.parse(req.response);
                   var move = j.move;
                    console.log('Making move:', move);
                };

                    req.send(event.data);
                }
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


