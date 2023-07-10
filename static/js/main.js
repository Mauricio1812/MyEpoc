/**
 * 
 */
let chatName = ''
let chatSocket = null
let chatWindowUrl = window.location.href
let chatRoomUuid = Math.random().toString(36).slice(2, 12)

/**
 * Elements
 */
const user_name = document.querySelector('#user_name').textContent.replaceAll('"','')

const chatElements = document.querySelector('#chat')
const chatOpenElement = document.querySelector('#chat_open')
const chatIconElement = document.querySelector('#chat_icon')

const chatRoomElement = document.querySelector('#chat_room')

const chatLogElement = document.querySelector('#chat_log')
const chatInputlement = document.querySelector('#chat_message_input')
const chatSubmitElement = document.querySelector('#chat_message_submit')


/**
 * Functions
 */
function scrollToBottom(){
    chatLogElement.scrollTop = chatLogElement.scrollHeight
}


function getCookie(name){
    var cookieValue = null

    if (document.cookie && document.cookie != ''){
        var cookies = document.cookie.split(';')

        for (var i=0; i < cookies.length; i++){
            var cookie = cookies[i].trim()
            console.log(cookie)
            if (cookie.substring(0, name.length+1) === (name + '=')){
                cookieValue = decodeURIComponent(cookie.substring(name.length+1))
                console.log(cookieValue)
                break
            }
        }
    }

    return cookieValue
}

function sendMessage(){
    chatSocket.send(JSON.stringify({
        'type': 'message',
        'message': chatInputlement.value,
        'name': user_name,
    }))

    chatInputlement.value = ''
}

function OnChatmessage(data){
    console.log('onChatMessage', data)

    if (data.type == 'chat_message'){
        if (data.agent){
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

async function joinChatRoom(){

    console.log('Join as: ', user_name)
    console.log('Room: ', chatRoomUuid)

    const data = new FormData()
    data.append('name', user_name)
    data.append('url', chatWindowUrl)
    
    await fetch(`chat/api/create-room/${chatRoomUuid}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        body:data,
    })
    .then(function(res){
        return res.json()
    })
    .then(function(data){
        console.log('data', data)
    })

    chatSocket = new WebSocket(`ws://${window.location.host}/ws/${chatRoomUuid}/`)

    chatSocket.onmessage = function(e){
        console.log('OnMessage')

        OnChatmessage(JSON.parse(e.data))
    }

    chatSocket.onopen = function(e){
        console.log('OnOpen - chat socket was opened')
        scrollToBottom()
    }

    chatSocket.onclose = function(e){
        console.log('OnClose - chat socket was closed')
    }

}

/**
 * Event listeners
 */
chatOpenElement.onclick = function(e){
    e.preventDefault()

    chatIconElement.classList.add('hidden')
    chatRoomElement.classList.remove('hidden')
    
    joinChatRoom()

    return false
}

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