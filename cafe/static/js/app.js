let openShopping = document.querySelector('.shopping');
let closeShopping = document.querySelector('.closeShopping');
let list = document.querySelector('.list');
let listCard = document.querySelector('.listCard');
let body = document.querySelector('body');
let total = document.querySelector('.total');
let quantity = document.querySelector('.quantity');

document.addEventListener("DOMContentLoaded", function() {
    // Now you can use the drink_list in your JavaScript code
    console.log(drink_list);
    // Do something with drink_list
});

openShopping.addEventListener('click', ()=>{
    body.classList.add('active');
})

closeShopping.addEventListener('click', ()=>{
    body.classList.remove('active');
})


let listCards  = [];

function initApp()
{
    drink_list.forEach((value, key) =>{
        let newDiv = document.createElement('div');
        newDiv.classList.add('item');
        newDiv.innerHTML = `
            <img src="${value.img_src}">
            <div class="title">${value.name}</div>
            <div class="price">${value.price.toLocaleString()}đ</div>
            <button onclick="addToCard(${key})">Add to Card</button>
            `;
        list.appendChild(newDiv);
    })
}

initApp();

function addToCard(key)
{
    if(listCards[key] == null)
    {
        // copy product form list to list card
        listCards[key] = JSON.parse(JSON.stringify(drink_list[key]));
        listCards[key].quantity = 1;
    } 
    reloadCard();
}

function reloadCard()
{
    listCard.innerHTML = '';
    let count = 0;
    let totalPrice = 0;
    listCards.forEach((value, key)=>{
        totalPrice = totalPrice + value.price;
        count = count + value.quantity;
        if(value != null)
        {
            let newDiv = document.createElement('li');
            newDiv.innerHTML = `
                <div><img src="${value.img_src}"/></div>
                <div>${value.name}</div>
                <div>${value.price.toLocaleString()}</div>
                <div>
                    <button onclick="changeQuantity(${key}, ${value.quantity - 1})">-</button>
                    <div class="count">${value.quantity}</div>
                    <button onclick="changeQuantity(${key}, ${value.quantity + 1})">+</button>
                </div>
                <form class = "Takenot">
                    <label for = "noteInput_${key}"> Note </label>
                    <Input id = "noteInput_${key}"  class="Takenote" type = "text" placeholder = "Your preferences..."></input>
                </form>`;
                listCard.appendChild(newDiv);
        }
    })
    total.innerText = totalPrice.toLocaleString();
    quantity.innerText = count;
}

function changeQuantity(key, quantity)
{
    let total = 0;
    if(quantity == 0)
    {
        delete listCards[key];
    }
    else
    {
        listCards[key].quantity = quantity;
        total = quantity * drink_list[key].price;
        listCards[key].price = total;
    }
    reloadCard();
}

function submitOrder() {
    const orderData = {
        order: []
    };

    listCards.forEach((value, key) => {
        if (value != null) {
            const noteInput = document.querySelector(`#noteInput_${key}`);
            const noteValue = noteInput ? noteInput.value : "";

            orderData.order.push({
                _id: value._id.$oid,
                name: value.name,
                quantity: value.quantity,
                note: noteValue
            });
        }
    });
    // Call the function to send the POST request
    sendPostRequest(orderData);
    
}

function sendPostRequest(orderData) {
    fetch(window.location.href, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(orderData)
    })
    .then(response => response.json())
    .then(data => {
        // Handle the response from the server (if needed)
        console.log('Server response:', data);
        alert(data.message);
        // Clear the shopping cart after a successful order
        listCards = [];
        reloadCard();
        body.classList.remove('active');
    })
    .catch(error => {
        console.error('Error sending POST request:', error);
        alert(error);
        // Handle the error (e.g., show an alert to the user)
    });
}
