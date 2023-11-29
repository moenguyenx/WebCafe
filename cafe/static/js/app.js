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
            <button onclick="addToCard(${key})">Add To Card</button>`;
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
                </div>`;
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
    }else
    {
        listCards[key].quantity = quantity;
        total = quantity * drink_list[key].price;
        listCards[key].price = total;
    }
    reloadCard();
    return total;
}