console.log('Hello John. You already won')

var updateBtns = document.getElementsByClassName("update-cart")

for (var i = 0 ; i< updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var eventId = this.dataset.event
        var action = this.dataset.action
        console.log('eventId:',eventId, 'action:', action)

        console.log("USER:",user)
        if(user === 'AnonymousUser'){
            console.log('User is not logged in')
        }else{
           updateUserOrder(eventId,action)
        }
    })
}

function updateUserOrder(eventId,action){
    var url = '/update_item/'

    fetch(url,{
        method: 'POST',
        headers: {
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({
            'eventId':eventId,
            'action':action
        })
        })
   .then((response) => {
            return response.json()
        })
    .then((data) => {
            console.log('data:',data)
            location.reload()
        })
    

}