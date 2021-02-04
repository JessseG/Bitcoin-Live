// let buyLimitPrice = document.getElementById("buy-limit-price");
// let buyLimitQuantity = document.getElementById("buy-limit-quantity");
// let sellLimitPrice = document.getElementById("sell-limit-price");
// let sellLimitQuantity = document.getElementById("sell-limit-quantity");

// $("#maximize-buy").click(function (event) {
//   event.preventDefault();
//   $.ajax({
//     url: "/max_buy",
//     type: "POST",
//     data: {
//       buySymbol: $("#select-buy-limit-symbol").val(),
//       buyPrice: $("#buy-limit-price").val(),
//     },
//     success: function (result) {
//       buyLimitQuantity.value = result.maxBuy;
//       // console.log(result.maxBuy);
//     },
//     error: function (result) {
//       alert("Invalid Input");
//     },
//   });
// });

// $("#maximize-sell").click(function (event) {
//   event.preventDefault();
//   $.ajax({
//     url: "/max_sell",
//     type: "POST",
//     data: {
//       sellSymbol: $("#select-sell-limit-symbol").val(),
//       sellPrice: $("#sell-limit-price").val(),
//     },
//     success: function (result) {
//       sellLimitQuantity.value = result.maxSell;
//       // console.log(result.maxSell);
//     },
//     error: function (result) {
//       alert("Invalid Input");
//     },
//   });
// });

//________________________________________________________________________

// document.getElementById("buy-limit-plus-ten").addEventListener("click", () => {
//   if (!buyLimitPrice.value) {
//     buyLimitPrice.value = 0;
//   }
//   buyLimitPrice.value = parseFloat(buyLimitPrice.value) + 10;
// });
// document.getElementById("buy-limit-minus-ten").addEventListener("click", () => {
//   if (!buyLimitPrice.value) {
//     buyLimitPrice.value = 0;
//   }
//   buyLimitPrice.value = parseFloat(buyLimitPrice.value) - 10;
// });
// document.getElementById("sell-limit-plus-ten").addEventListener("click", () => {
//   if (!sellLimitPrice.value) {
//     sellLimitPrice.value = 0;
//   }
//   sellLimitPrice.value = parseFloat(sellLimitPrice.value) + 10;
// });
// document
//   .getElementById("sell-limit-minus-ten")
//   .addEventListener("click", () => {
//     if (!sellLimitPrice.value) {
//       sellLimitPrice.value = 0;
//     }
//     sellLimitPrice.value = parseFloat(sellLimitPrice.value) - 10;
//   });

//________________________________________________________________________

// var binanceSocketLivePrice = new WebSocket(
//   "wss://stream.binance.com:9443/ws/btcusdt@ticker"
// );

// tradeSymbols = ["BTCUSDT", "BTCEUR", "EURUSDT"];

// for (let i = 0; i < tradeSymbols.length; i++) {
//   eval(
//     `var priceSocket_${tradeSymbols[i]} = new WebSocket("wss://stream.binance.com:9443/ws/${tradeSymbols[i]}@ticker");`
//   );
// }

// // Partyle determines default candlestick size
// var priceSocket = priceSocket_BTCUSDT;

// document.getElementById("select-trade").addEventListener("change", function () {

//   livePriceSocket = eval(`priceSocket_${this.value}`);

//   fetch(`http://localhost:5000/${this.value}_candles`)

//     .then((r) => r.json())
//     .then((response) => {

//       response.pop();
//       console.log(response);
//       candleSeries.setData(response);
//     });

//   socket.removeEventListener("message", updateCandles);
//   socket.addEventListener("message", updateCandles);
// });

// var prevPrice;

// var priceIndicator = document.getElementById("real-time-price");

// var newPrice;

// binanceSocketLivePrice.onmessage = function (event) {
//   var message = JSON.parse(event.data);
//   //   console.log(message);

//   newPrice = parseFloat(message.c).toFixed(2);

//   // FAST PRICE ______________________________________

//   var lastPriceBL = document.getElementById("buy-limit-fast-price");
//   var lastPriceSL = document.getElementById("sell-limit-fast-price");

//   lastPriceBL.onclick = function () {
//     price = parseFloat(newPrice);
//     // price -= 10;
//     buyLimitPrice.value = Math.floor(price - 5);
//     console.log(buyLimitPrice.value);
//   };

//   lastPriceSL.onclick = function () {
//     price = parseFloat(newPrice);
//     // price -= 10;
//     sellLimitPrice.value = Math.floor(price + 5);
//     console.log(sellLimitPrice.value);
//   };

//   // PRICE BAR ____________________________________

//   if (newPrice > prevPrice) {
//     priceIndicator.innerText = `$ ${newPrice
//       .toString()
//       .replace(/\B(?=(\d{3})+(?!\d))/g, ",")}`;
//     priceIndicator.style = "color: rgb(0, 190, 10);";
//   } else if (newPrice < prevPrice) {
//     priceIndicator.innerText = `$ ${newPrice
//       .toString()
//       .replace(/\B(?=(\d{3})+(?!\d))/g, ",")}`;
//     priceIndicator.style = "color: #ff3b3b;";
//   } else if (newPrice === prevPrice) {
//     priceIndicator.innerText = `$ ${newPrice
//       .toString()
//       .replace(/\B(?=(\d{3})+(?!\d))/g, ",")}`;
//     priceIndicator.style = "color: white;";
//   }

//   prevPrice = newPrice;
// };

//________________________________________________________________________

// document.getElementById("sell-limit-price").value;

// var lastPrice = document.getElementById("buy-limit-last-price");

// lastPrice.addEventListener("click", () => {
//   console.log(newPrice);
// buyLimitPrice.value = parseFloat(priceIndicator.innerText);
// console.log(buyLimitPrice.innerText);
// buyLimitPrice.value = parseFloat(buyLimitPrice.value) + 10;
// });
// NOT WORKING ^

// document.getElementById("trade-history").innerHTML = (
//   <table>
//     <tr>
//       <td id="asset"></td>
//       <td id="value"></td>
//     </tr>
//   </table>
// );

// ORDERS
// {
//     "symbol": "BTCEUR",
//     "orderId": 297659224,
//     "orderListId": -1,
//     "clientOrderId": "web_f4c366c7c47f4c2dbfaa2b6d6c41d105",
//     "price": "0.00000000",
//     "origQty": "0.00072500",
//     "executedQty": "0.00072500",
//     "cummulativeQuoteQty": "20.12809525",
//     "status": "FILLED",
//     "timeInForce": "GTC",
//     "type": "MARKET",
//     "side": "SELL",
//     "stopPrice": "0.00000000",
//     "icebergQty": "0.00000000",
//     "time": 1612148083599,
//     "updateTime": 1612148083599,
//     "isWorking": True,
//     "origQuoteOrderQty": "0.00000000"
//   },

// TRADES
// {
//   "symbol": "BTCEUR",
//   "id": 8299412,
//   "orderId": 186600884,
//   "orderListId": -1,
//   "price": "26000.00000000",
//   "qty": "0.00084500",
//   "quoteQty": "21.97000000",
//   "commission": "0.00000000",
//   "commissionAsset": "BTC",
//   "time": 1609738672314,
//   "isBuyer": True,
//   "isMaker": True,
//   "isBestMatch": True
// },

//___________________________________________________________________________________

// $(window).ready(function (event) {
//   // event.preventDefault();
//   $.ajax({
//     url: "/default",
//     type: "POST",
//     data: {
//       symbol: "BTCUSDT",
//     },
//     success: function (result) {
//       result.pop();
//       candleSeries.setData(result);
//     },
//     error: function (result) {
//       alert("Invalid Input");
//     },
//     start_time: new Date().getTime(),
//     complete: function (data) {
//       console.log(
//         "This request took " + (new Date().getTime() - this.start_time) + " ms"
//       );
//     },
//   });
// });

//___________________________________________________________________________________

function fillTable(data) {
  function isBuyer(value) {
    let side = eval(JSON.stringify(value));
    // console.log(value);
    if (side) {
      return "BUY";
    } else if (!side) {
      return "SELL";
    }
  }

  //Add items to shopping table
  let trades_table = document.getElementById("trade-history-table");
  for (let i = data.length - 1; i > data.length - 5; i--) {
    trades_table.innerHTML +=
      "<tr><td>" +
      data[i].symbol +
      "</td><td>" +
      isBuyer(data[i].isBuyer) +
      "</td><td>" +
      Math.floor(data[i].price) +
      "</td><td>" +
      data[i].qty +
      "</td><td>" +
      data[i].commission +
      "</td><td>" +
      parseFloat(data[i].quoteQty).toFixed(2) +
      "</td></tr>";
  }
  // let row1 = document.querySelectorAll(
  //   "#trade-history-table tr:first-of-type td"
  // );
  // $(row1).css("padding-top", "2vh");
}

$(document).ready(function (event) {
  // event.preventDefault();
  $.ajax({
    url: "/trade_history",
    type: "POST",
    data: {
      symbol: "BTCEUR",
    },
    success: function (result) {
      // console.log(result);
      fillTable(result);
    },
    error: function (result) {
      alert("Invalid Input — Trade History");
    },
  });
});
