function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}


let onAction = false,
    lastid = "-1",
    conversation = "0",
    size = "1";


function sendNotification(title, options) {
    let notification = undefined;
    if (!("Notification" in self)) {
        console.warn("browser does not support notifications");
    } else if (Notification.permission === "granted") {
        notification = new Notification(title, options);
    } else if (Notification.permission !== 'denied') {
        Notification.requestPermission(permission => {
            if (permission === 'granted') {
                notification = new Notification(title, options);
            } else {
                // пользователь отклонил запрос на отправку сообщений
                console.log("user denied request on notifications");
            }
        })
    } else {
        // пользователь давно отказал в показе сообщений
        console.log("messages are denied by user policy");
    }

    if (notification !== undefined) {
        notification.onclick = () => {
            self.focus();
            notification.close();
        };
        };

    }


function getAfterPromise() {
    return new Promise((done, fail)=>{
        console.log('run get-after promise');

        let xhr = new XMLHttpRequest();

        let params = "conversation=" + encodeURIComponent(conversation) + "&afterid=" + encodeURIComponent(lastid);
        params += "&size=" + encodeURIComponent(size);
        console.log(params);
        xhr.open('GET', '/message/get-after?' + params, false);

        // 3. Отсылаем запрос
        xhr.send();

        // 4. Если код ответа сервера не 200, то это ошибка
        if (xhr.status != 200) {
          // обработать ошибку
            console.warn("xhr error: " + xhr.status + ': ' + xhr.statusText ); // пример вывода: 404: Not Found
            fail("xhr error: " + xhr.status + ': ' + xhr.statusText);
        } else {
          // вывести результат
            // console.log( xhr.responseText ); // responseText -- текст ответа.
            done(xhr.responseText);
        }
    })
}

async function work() {
    while (true) {
        if (onAction) {
            let wait_for = getAfterPromise();
            wait_for.then(
                (data)=> {
                    console.log(data);
                    if (JSON.parse(data).length > 0) {
                        onAction = false;
                        sendNotification('Ofty', {body: 'У вас есть новые сообщения.', icon: 'favicon.svg', dir: 'ltr', tag: 'ofty'})
                        postMessage(data);
                    }
                },
                (error)=> {console.warn(error);}
            );
            Promise.all([wait_for]);
        }
        await sleep(2010);
    }
}

onmessage = (messageEvent)=>{
    let data = messageEvent.data;
    if (data === "pause") {
        onAction = false;
    } else if (data === "start") {
        if (onAction === false) {
            onAction = true;
        }
    }

    if (data.hasOwnProperty("lastid")) {
        lastid = data.lastid;
    }

    if (data.hasOwnProperty("conversation")) {
        conversation = data.conversation;
    }

    if (data.hasOwnProperty("size")) {
        size = data.size;
    }
};
console.log(1);
work();
