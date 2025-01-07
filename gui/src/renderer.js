const { ipcRenderer } = require('electron')

document.addEventListener('DOMContentLoaded', () => {
    // 윈도우 컨트롤 이벤트
    document.querySelector('.minimize').addEventListener('click', () => {
        ipcRenderer.send('minimize-window')
    })

    document.querySelector('.maximize').addEventListener('click', () => {
        ipcRenderer.send('maximize-window')
    })

    document.querySelector('.close').addEventListener('click', () => {
        ipcRenderer.send('close-window')
    })

    const textarea = document.getElementById('userInput')
    const sendButton = document.querySelector('.send-button')
    const messagesContainer = document.getElementById('messages')

    // 텍스트 영역 자동 크기 조절
    textarea.addEventListener('input', function() {
        this.style.height = 'auto'
        this.style.height = this.scrollHeight + 'px'
    })

    // 메시지 전송 함수
    function sendMessage() {
        const message = textarea.value.trim()
        if (message) {
            // 사용자 메시지 추가
            addMessage(message, 'user')
            // AI 응답 (여기에 실제 AI 통신 로직 추가 필요)
            setTimeout(() => {
                addMessage('AI의 응답입니다.', 'ai')
            }, 1000)
            
            textarea.value = ''
            textarea.style.height = 'auto'
        }
    }

    // 메시지 추가 함수
    function addMessage(text, type) {
        const messageDiv = document.createElement('div')
        messageDiv.classList.add('message', `${type}-message`)
        messageDiv.textContent = text
        messagesContainer.appendChild(messageDiv)
        messagesContainer.scrollTop = messagesContainer.scrollHeight
    }

    // 이벤트 리스너
    sendButton.addEventListener('click', sendMessage)
    textarea.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault()
            sendMessage()
        }
    })
}) 