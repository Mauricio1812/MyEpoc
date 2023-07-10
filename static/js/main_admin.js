/**
 * Variables
 */

const chatRoom = document.querySelector('#room_uuid').textContent.replaceAll('"','')
const user_name = document.querySelector('#user_name').textContent.replaceAll('"','')
const user_id = document.querySelector('#user_id').textContent.replaceAll('"','')

let chatSocket = null

/**
 * Elements
 */
const chatLogElement = document.querySelector('#chat_log')
const chatInputlement = document.querySelector('#chat_message_input')
const chatSubmitElement = document.querySelector('#chat_message_submit')

/**
 * Functions
 */
function scrollToBottom(){
    chatLogElement.scrollTop = chatLogElement.scrollHeight
}

function OnChatmessage(data){
    console.log('onChatMessage', data)

    if (data.type == 'chat_message'){
        if (!data.agent){
            //If agent sent message
            chatLogElement.innerHTML += `
                <div class="flex w-full mt-2 space-x-3 max-w-md">
                <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300 text-center pt-2">${data.initials}</div>
                
                <div>
                    <div class="bg-gray-300 p-3 rounded-l-lg rounded-br-lg">
                        <p class="text-sm">${data.message}</p>
                    </div>

                    <span class="text-xs text-gray-500 leading-none"> ${data.created_at} ago</span>
                    </div>
                </div>`
        }else{ 
            //If client sent message
            chatLogElement.innerHTML += `
                <div class="flex w-full mt-2 space-x-3 max-w-md ml-auto justify-end">

                <div>
                    <div class="bg-blue-300 p-3 rounded-l-lg rounded-br-lg">
                        <p class="text-sm">${data.message}</p>
                    </div>

                    <span class="text-xs text-gray-500 leading-none"> ${data.created_at} ago</span>
                    </div>

                    <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300 text-center pt-2">${data.initials}</div>
                </div>`
        }
    }

    scrollToBottom()
}

function sendMessage(){
    chatSocket.send(JSON.stringify({
        'type': 'message',
        'message': chatInputlement.value,
        'name': user_name,
        'agent': user_id,
    }))

    chatInputlement.value = ''
}


/**
 * WebSocket
 */

chatSocket = new WebSocket(`ws://${window.location.host}/ws/${chatRoom}/`)


chatSocket.onmessage = function(e){
    console.log('OnMessage')

    OnChatmessage(JSON.parse(e.data))
}

chatSocket.onopen = function(e){
    console.log('on_open')
    scrollToBottom()
}

chatSocket.onclose  = function(e){
    console.log('socket closeed unexpectedly')
}

/**
 * Event lister
 */
chatSubmitElement.onclick = function(e){
    e.preventDefault()
    sendMessage()
    return false
}

chatInputlement.onkeyup = function(e){
    if(e.keyCode == 13){
        sendMessage()
    }
}