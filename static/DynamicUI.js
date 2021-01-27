let buyLimitPrice = document.getElementById("buy-limit-price");
let buyLimitQuantity = document.getElementById("buy-limit-quantity");
let sellLimitPrice = document.getElementById("sell-limit-price");
let sellLimitQuantity = document.getElementById("sell-limit-quantity");

$("#maximize-buy").click(function (event) {
  event.preventDefault();
  $.ajax({
    url: "/max_buy",
    type: "POST",
    data: {
      buyPrice: $("#buy-limit-price").val(),
    },
    success: function (result) {
      buyLimitQuantity.value = result.maxBuy;
      // console.log(result.maxBuy);
    },
    error: function (result) {
      alert("Invalid Input");
    },
  });
});

$("#maximize-sell").click(function (event) {
  event.preventDefault();
  $.ajax({
    url: "/max_sell",
    type: "POST",
    data: {
      sellPrice: $("#sell-limit-price").val(),
    },
    success: function (result) {
      sellLimitQuantity.value = result.maxSell;
      // console.log(result.maxSell);
    },
    error: function (result) {
      alert("Invalid Input");
    },
  });
});

document.getElementById("buy-limit-plus-ten").addEventListener("click", () => {
  if (!buyLimitPrice.value) {
    buyLimitPrice.value = 0;
  }
  buyLimitPrice.value = parseFloat(buyLimitPrice.value) + 10;
});
document.getElementById("buy-limit-minus-ten").addEventListener("click", () => {
  if (!buyLimitPrice.value) {
    buyLimitPrice.value = 0;
  }
  buyLimitPrice.value = parseFloat(buyLimitPrice.value) - 10;
});
document.getElementById("sell-limit-plus-ten").addEventListener("click", () => {
  if (!sellLimitPrice.value) {
    sellLimitPrice.value = 0;
  }
  sellLimitPrice.value = parseFloat(sellLimitPrice.value) + 10;
});
document
  .getElementById("sell-limit-minus-ten")
  .addEventListener("click", () => {
    if (!sellLimitPrice.value) {
      sellLimitPrice.value = 0;
    }
    sellLimitPrice.value = parseFloat(sellLimitPrice.value) - 10;
  });

var binanceSocketLivePrice = new WebSocket(
  "wss://stream.binance.com:9443/ws/btcusdt@ticker"
);

var prevPrice;

var priceIndicator = document.getElementById("real-time-price");

binanceSocketLivePrice.onmessage = function (event) {
  //   console.log("new MESSAGE");
  var message = JSON.parse(event.data);

  //   var candleStick = message.k;

  var newPrice = parseFloat(message.c).toFixed(2);

  if (newPrice > prevPrice) {
    priceIndicator.innerText = `$ ${newPrice
      .toString()
      .replace(/\B(?=(\d{3})+(?!\d))/g, ",")}`;
    priceIndicator.style = "color: rgb(0, 190, 10);";
  } else if (newPrice < prevPrice) {
    priceIndicator.innerText = `$ ${newPrice
      .toString()
      .replace(/\B(?=(\d{3})+(?!\d))/g, ",")}`;
    priceIndicator.style = "color: #ff3b3b;";
  } else if (newPrice === prevPrice) {
    priceIndicator.innerText = `$ ${newPrice
      .toString()
      .replace(/\B(?=(\d{3})+(?!\d))/g, ",")}`;
    priceIndicator.style = "color: white;";
  }

  prevPrice = newPrice;
};
