### Message API

/message/로 접근

Ex) /message/send/

```python
    path('send/', views.SendMessage.as_view(), name='send_message'),
    # 쪽지 보내기
    # Post method
    # need user credential
    title: null, blank True
    content: null, blank True
    receiver: receiver's username(유저 네임이 없으면 에러)
        
    "id": 52,
    "title": "test",
    "sent_at": "2019-06-03T05:22:59.494020Z",
    "content": "test",
    "receiver": "yuna"
        
    path('box/', views.GetMessageBox.as_view(), name='message_box'),
    # request.user의 쪽지함
    # GET method
    # need user credential
    
    "id": 2,
    "owner": "t1",
    "messages": [
        {
            "id": 48,
            "title": "t",
            "sender": "t1",
            "sent_at": "2019-06-02T14:40:43.669805Z",
            "receiver": "yuna"
        },
        {
            "id": 49,
            "title": "49",
            "sender": "t1",
            "sent_at": "2019-06-02T14:41:31.428303Z",
            "receiver": "yuna"
        }
    ]
    
    path('box/sent/', views.GetSentMessageBox.as_view(), name='sent_message_box')
    # 보낸 메시지 함
    # method: GET
    # box/와 형식이 동일. 단, request.user==sender인 메시지들만 list up.
    
    path('box/received/', views.GetReceivedMessageBox.as_view(), name='received_message_box')
    # 받은 메시지 함
    # method: GET
    # box/와 형식이 동일. 단, request.user==receiver인 메시지들만 list up.
    
    path('<int:message_id>/', views.GetMessage.as_view(), name='get_message')
    # message_id의 쪽지
    # GET method
    # need user credential(permission 추가 예정)
    
    "id": 1,
    "title": "title",
    "sent_at": "2019-06-02T08:55:33.056232Z",
    "content": "content",
    "sender": "t1",
    "receiver": "yuna",
    "is_read": false,
    "message_box": [
        3
    ]
    
    path('unread/num/', views.GetUnreadMessageNum, name='unread_num')
    # 읽지 않은 메시지의 개수를 반환
    # method: GET
    GET 형식
    {"num": 3}
```

