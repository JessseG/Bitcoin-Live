symbols = ["btcusdt", "btceur", "eurusdt"];

// Sockets for real-time ticker
for (let i = 0; i < symbols.length; i++) {
  eval(
    `var priceSocket_${symbols[i]} = new WebSocket("wss://stream.binance.com:9443/ws/${symbols[i]}@ticker");`
  );
}

var priceSocket = priceSocket_btcusdt;
var prevPrice;
var newPrice;

var priceIndicator = document.getElementById("real-time-price");
var percentChange24Hour = document.getElementById("real-24h-change");
var high24Hour = document.getElementById("real-24h-high");
var low24Hour = document.getElementById("real-24h-low");
var base24HourVolume = document.getElementById("real-24h-base-volume");
var quote24HourVolume = document.getElementById("real-24h-quote-volume");

var baseDisplay = "none";
var quoteDisplay = "inline-block";

quote24HourVolume.style.display = quoteDisplay;
base24HourVolume.style.display = baseDisplay;

function updatePriceTicker(event) {
  var message = JSON.parse(event.data);
  // console.log(message.c);
  let symbol = document.getElementById("select-trade").value;
  let sign;

  if (symbol === "BTCUSDT") {
    newPrice = parseFloat(message.c).toFixed(2);
    sign = "$";
  } else if (symbol === "BTCEUR") {
    newPrice = parseFloat(message.c).toFixed(2);
    sign = "€";
  } else if (symbol === "EURUSDT") {
    newPrice = parseFloat(message.c).toFixed(4);
    sign = "$";
  }

  // PRICE BAR ____________________________________

  if (newPrice > prevPrice) {
    if (symbol === "EURUSDT") priceIndicator.innerText = `${sign} ${newPrice}`;
    else {
      priceIndicator.innerText = `${sign} ${newPrice
        .toString()
        .replace(/\B(?=(\d{3})+(?!\d))/g, ",")}`;
    }
    priceIndicator.style = "color: rgb(0, 190, 10);"; // green
  } else if (newPrice < prevPrice) {
    if (symbol === "EURUSDT") priceIndicator.innerText = `${sign} ${newPrice}`;
    else {
      priceIndicator.innerText = `${sign} ${newPrice
        .toString()
        .replace(/\B(?=(\d{3})+(?!\d))/g, ",")}`;
    }
    priceIndicator.style = "color: #ff3b3b;"; // red
  } else if (newPrice === prevPrice) {
    if (symbol === "EURUSDT") priceIndicator.innerText = `${sign} ${newPrice}`;
    else {
      priceIndicator.innerText = `${sign} ${newPrice
        .toString()
        .replace(/\B(?=(\d{3})+(?!\d))/g, ",")}`;
    }
    priceIndicator.style = "color: white;";
  }

  prevPrice = newPrice;
  let percentChanged = parseFloat(message.P).toFixed(2);

  if (parseFloat(message.P) > 0) {
    percentChange24Hour.innerText = `+ ${percentChanged}%`;
    percentChange24Hour.style =
      "color: rgb(0, 190, 10); font-size: 2vh; letter-spacing: 0.4px"; // green
  } else if (parseFloat(message.P) < 0) {
    percentChange24Hour.innerText = `${percentChanged}%`;
    percentChange24Hour.style =
      "color: #ff3b3b; font-size: 2vh; letter-spacing: 0.4px"; // red
  } else if (parseFloat(message.P) === 0) {
    percentChange24Hour.innerText = `${percentChanged}%`;
    percentChange24Hour.style =
      "color: white; font-size: 2vh; letter-spacing: 0.4px"; // white
  }

  let lowPrice24Hour;
  let highPrice24Hour;

  if (symbol === "EURUSDT") {
    lowPrice24Hour = parseFloat(message.l);
    highPrice24Hour = parseFloat(message.h);
  } else {
    lowPrice24Hour = Math.floor(parseFloat(message.l))
      .toString()
      .replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    highPrice24Hour = Math.floor(parseFloat(message.h))
      .toString()
      .replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  }

  high24Hour.innerText = `${sign} ${highPrice24Hour}`;
  high24Hour.style = "color: white; font-size: 2vh;"; // light-blue

  low24Hour.innerText = `${sign} ${lowPrice24Hour}`;
  low24Hour.style = "color: white; font-size: 2vh;"; // light-blue

  let base24HourVol = Math.floor(parseFloat(message.v))
    .toString()
    .replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  let baseAsset = symbol.substring(0, 3);

  base24HourVolume.innerText = `${base24HourVol} ${baseAsset}`;
  base24HourVolume.style = `display: ${baseDisplay}; color: rgb(255, 224, 51); font-size: 2vh;`; // gold

  function convertNumber(num) {
    let modNum = "";
    if (num >= 1e9) {
      modNum = (num / 1e9).toFixed(2).toString() + " Billion";
    } else if (num >= 1e6 && num < 1e9) {
      modNum = (num / 1e6).toFixed(2).toString() + " Million";
    }

    return modNum;
  }

  let quoteAsset = symbol.substring(3);
  // console.log(quoteAsset);

  let quote24HourVol = convertNumber(Math.floor(parseFloat(message.q)));
  if (quoteAsset === "USDT") {
    quote24HourVolume.innerText = `$ ${quote24HourVol}`;
    quote24HourVolume.style = `display: ${quoteDisplay}; color: rgb(0, 190, 10); font-size: 2vh;`; // green
  } else if (quoteAsset === "EUR") {
    quote24HourVolume.innerText = `€ ${quote24HourVol}`;
    quote24HourVolume.style = `display: ${quoteDisplay}; color: rgb(69, 196, 255); font-size: 2vh;`; // blue
  } else {
    quote24HourVolume.innerText = `${quote24HourVol} ${quoteAsset}`;
    quote24HourVolume.style = `display: ${quoteDisplay}; color: rgb(255, 224, 51); font-size: 2vh;`; // gold
  }
}
//_____________________________________________________

let assetFlip = 1;
function flipAsset() {
  // console.log("flip");
  if (assetFlip % 2 === 0) {
    baseDisplay = "none";
    quoteDisplay = "inline-block";
  } else if (assetFlip % 2 === 1) {
    baseDisplay = "inline-block";
    quoteDisplay = "none";
  }
  assetFlip++;
}

let flipIcon = document.getElementById("flip-asset-icon");
flipIcon.addEventListener("click", flipAsset);

// FAST PRICE ______________________________________

var lastPriceBL = document.getElementById("buy-limit-fast-price");
var lastPriceSL = document.getElementById("sell-limit-fast-price");

lastPriceBL.onclick = function () {
  price = parseFloat(newPrice);
  // price -= 10;
  // buyLimitPrice.value = Math.floor(price - 5);
  if (price > 1000) buyLimitPrice.value = Math.floor(price);
  else if (price > 10 && price < 1000)
    buyLimitPrice.value = Math.round((price + Number.EPSILON) * 100) / 100;
  else buyLimitPrice.value = price;
  // console.log(buyLimitPrice.value);
};

lastPriceSL.onclick = function () {
  price = parseFloat(newPrice);
  // price -= 10;
  // sellLimitPrice.value = Math.floor(price + 5);
  if (price > 1000) sellLimitPrice.value = Math.floor(price);
  else if (price > 10 && price < 1000)
    sellLimitPrice.value = Math.round((price + Number.EPSILON) * 100) / 100;
  else sellLimitPrice.value = price;
  // console.log(sellLimitPrice.value);
};

window.onload = function () {
  priceSocket.addEventListener("message", updatePriceTicker);
  // base24HourVolume.style = "display: inline-block;";
  // quote24HourVolume.style = "display: none;";
  // console.log(quote24HourVolume.style.display);
  // console.log(base24HourVolume.style.display);
};

//________________________________________________________________________________________________________

let heightRatio = 0.557; // 0.63
let widthRatio = 0.75; // 0.71 works on heroku with a row-1-column-1 & row-2-column-1 width: 72.5% CSS

let w = window.innerWidth * widthRatio; //1060 - bigger
let h = window.innerHeight * heightRatio; //537 - smaller

// console.log(window.innerWidth);
// console.log(window.innerHeight);
// console.log();

function reportWindowSize() {
  // heightOutput.textContent = window.innerHeight;
  // widthOutput.textContent = window.innerWidth;
  // console.log(window.innerWidth);
  // console.log(window.innerHeight);
  chart.resize(
    window.innerWidth * widthRatio,
    window.innerHeight * heightRatio
  );
}

var chart = LightweightCharts.createChart(document.getElementById("charts"), {
  width: w,
  height: h,
  layout: {
    backgroundColor: "#141411",
    textColor: "rgba(255, 255, 255, 0.9)",
    fontSize: 14.2,
    fontFamily: "Ubuntu",
    // backgroundColor: "#FAEBD7",
    // textColor: "#696969",
  },
  grid: {
    vertLines: {
      color: "#383838",
      width: 0.3,
    },
    horzLines: {
      color: "#383838",
      width: 0.3,
    },
  },
  crosshair: {
    mode: LightweightCharts.CrosshairMode.Normal,
  },
  priceScale: {
    borderColor: "rgba(197, 203, 206, 0.8)",
    size: 5,
    // position: " ",
    // mode: 3,
    // autoScale: false,
    // invertScale: true,
    // alignLabels: false,
    // borderVisible: true,
    // borderColor: "red",
  },
  timeScale: {
    borderColor: "rgba(197, 203, 206, 0.8)",
    timeVisible: true,
    secondsVisible: false,
    rightBarStaysOnScroll: true, //react-toggle it later
    // rightOffset: 12,
    // bottomOffset: 15,
    // barSpacing: 3,
    // fixLeftEdge: true,
    // lockVisibleTimeRangeOnResize: true,
    // borderVisible: false,
    // borderColor: "#fff000",
    // visible: true,
    // timeVisible: true,
    // secondsVisible: false,
    // tickMarkFormatter: (time, tickMarkType, locale) => {
    //   console.log(time, tickMarkType, locale);
    //   const year = LightweightCharts.isBusinessDay(time)
    //     ? time.year
    //     : new Date(time * 1000).getUTCFullYear();
    //   return String(year);
    // },
  },
});

// let container = document.getElementById("charts");

var candleSeries = chart.addCandlestickSeries({
  upColor: "#5fffff",
  downColor: "#ff3b3b",
  borderDownColor: "#ff3b3b",
  borderUpColor: "#5fffff",
  wickDownColor: "#ff3b3b",
  wickUpColor: "#5fffff",
});

candleSeries.applyOptions({
  priceFormat: {
    type: "price",
    precision: 0,
    minMove: 1,
  },
});

// function resize() {
//   chart.applyOptions({
//     width: $("#charts").width(),
//     height: $("#charts").height(),
//   });
// }

// new ResizeObserver(outputsize).observe($("#charts"));

//_____________________________________________________________________

// $(window).resize(function () {
//   if (this.resizeTO) clearTimeout(this.resizeTO);
//   this.resizeTO = setTimeout(function () {
//     $(this).trigger("resizeEnd");
//   }, 0);
// });

// $(window).bind("resizeEnd", function () {
//   $("#width").text($(this).width());
//   $("#height").text($(this).height());
// });
//_____________________________________________________________________

window.addEventListener("resize", reportWindowSize);

// if (window.location.href === "http://localhost:5000/") {
// fetch("http://localhost:5000/default")
//   .then((r) => r.json())
//   .then((response) => {
//     response.pop();
//     candleSeries.setData(response);
//   });
// }

let loader = document.querySelector(".lds-spinner");
let reloadBtn = document.getElementById("reload-chart-btn");

$(document).ready(function (event) {
  // event.preventDefault();
  $.ajax({
    url: "/default",
    type: "POST",
    data: {
      symbol: "BTCUSDT",
    },
    async: true,
    success: function (result) {
      result.pop();
      candleSeries.setData(result);
      loader.style.display = "none";
      socket.addEventListener("message", updateCandles);
    },
    start_time: new Date().getTime(),
    timeout: 33000,
    error: function (xmlhttprequest, textstatus, message) {
      if (new Date().getTime() - this.start_time > 60000) {
        loader.style = "display: none;";
        reloadBtn.style = "display: block;";
        reloadBtn.addEventListener("click", function () {
          location.reload();
        });
      } else {
        $.ajax(this);
        // console.log(textstatus);
        // location.reload();
        // alert("Error Loading Chart Please Reload");
      }
    },
    complete: function (data) {
      // console.log(
      //   "This request took " + (new Date().getTime() - this.start_time) + " ms"
      // );
    },
  });
});

candles = [
  "1m",
  "3m",
  "5m",
  "15m",
  "30m",
  "1h",
  "2h",
  "4h",
  "6h",
  "8h",
  "1d",
  "3d",
];

// var socketList = [];

// Sockets for updating candles
for (let i = 0; i < symbols.length; i++) {
  for (let j = 0; j < candles.length; j++) {
    eval(
      `var binanceSocket_${symbols[i]}_${candles[j]} = new WebSocket("wss://stream.binance.com:9443/ws/${symbols[i]}@kline_${candles[j]}");`
    );
  }
}

// Partyle determines default candlestick size
var socket = binanceSocket_btcusdt_4h;

var x = 0;
function updateCandles(e) {
  let message = JSON.parse(e.data);
  // console.log(socket);
  // for (let x=0; x < 1; x++) {
  //   console.log(message);
  // }
  let candleStick = message.k;
  candleSeries.update({
    time: candleStick.t / 1000,
    open: candleStick.o,
    high: candleStick.h,
    low: candleStick.l,
    close: candleStick.c,
  });
}
// console.log(socket);
// socket.addEventListener("message", updateCandles);

document.getElementById("reset-chart-icon").onclick = function (event) {
  chart.timeScale().scrollToRealTime(3);
  // chart.timeScale().resetTimeScale();
};

let candleSelectors = document.getElementsByClassName("select-candle-size");
for (let x = 0; x < candleSelectors.length; x++) {
  // candleSelectors[x].addEventListener("change", function () {
  // console.log(this.value);
  // console.log(socket);
  // fetch(`http://localhost:5000/${this.value}_candles`)
  //   .then((r) => r.json())
  //   .then((response) => {
  //     response.pop();
  //     candleSeries.setData(response);
  //   });

  $(eval(candleSelectors[x])).change(function (event) {
    event.preventDefault();
    loader.style.display = "block";
    let currentSymbol = $("#select-trade").val().toLowerCase();
    socket.removeEventListener("message", updateCandles);
    // console.log(event.target.id);
    // document.getElementById("ddBusinessCategory").value = "";
    // console.log(this.value);
    // console.log($("#select-trade").val());

    for (let x = 0; x < candleSelectors.length; x++) {
      if (candleSelectors[x].value === this.value) {
        candleSize = candleSelectors[x].value;
      } else {
        candleSelectors[x].value = "";
      }
    }
    socket = eval(`binanceSocket_${currentSymbol}_${this.value}`);

    $.ajax({
      url: "/generate_candles",
      type: "POST",
      data: {
        tradeSymbol: $("#select-trade").val(),
        candleSize: this.value,
      },
      success: function (result) {
        // var data = JSON.parse(result);
        // console.log(result);
        result.pop();
        candleSeries.setData(result);
        loader.style.display = "none";
        socket.addEventListener("message", updateCandles);
        // console.log(result.msg);
      },
      error: function (result) {
        alert("error");
      },
    });
  });
}

//___________________________________________________________________________________

let buyLimitPrice = document.getElementById("buy-limit-price");
let buyLimitPriceBox = document.getElementById("buy-limit-price-box");
let buyLimitQuantity = document.getElementById("buy-limit-quantity");
let sellLimitPrice = document.getElementById("sell-limit-price");
let sellLimitPriceBox = document.getElementById("sell-limit-price-box");
let sellLimitQuantity = document.getElementById("sell-limit-quantity");

$("#maximize-buy").click(function (event) {
  event.preventDefault();
  // let validator;
  if (buyLimitPrice.value) {
    // validator = true;
    $.ajax({
      url: "/max_buy",
      type: "POST",
      data: {
        buySymbol: $("#select-buy-limit-symbol").val(),
        buyPrice: $("#buy-limit-price").val(),
      },
      success: function (result) {
        buyLimitQuantity.value = result.maxBuy;
        // console.log(result.maxBuy);
        buyLimitPriceBox.style.border = "none";
      },
      error: function (result) {
        alert("Max-buy Error");
      },
    });
  } else if (!buyLimitPrice.value) {
    // validator = false;
    buyLimitPriceBox.style.border = "1px solid red";
    return "No Input";
  }
  // console.log(validator);
});

$("#maximize-sell").click(function (event) {
  event.preventDefault();
  if (sellLimitPrice.value) {
    $.ajax({
      url: "/max_sell",
      type: "POST",
      data: {
        sellSymbol: $("#select-sell-limit-symbol").val(),
        sellPrice: $("#sell-limit-price").val(),
      },
      success: function (result) {
        sellLimitQuantity.value = result.maxSell;
        // console.log(result.maxSell);
        sellLimitPriceBox.style.border = "none";
      },
      error: function (result) {
        alert("Max-sell Error");
      },
    });
  } else if (!sellLimitPrice.value) {
    sellLimitPriceBox.style.border = "1px solid red";
    return "No Input";
  }
});

// let autoTradeAmount = document.getElementById("maximize-auto-trade");
let autoTradeQuantity = document.getElementById("auto-trade-quantity");
let autoTradeBox = document.getElementById("auto-trade-box");

$("#maximize-auto-trade").click(function (event) {
  event.preventDefault();
  // console.log($("#select-trade").val());
  if ($("#select-trade").val()) {
    $.ajax({
      url: "/max_autotrade",
      type: "POST",
      data: {
        autoSymbol: $("#select-trade").val(),
        // sellSymbol: $("#select-autotrade-symbol").val(),
      },
      success: function (result) {
        autoTradeQuantity.value = result.maxAuto;
        // console.log(result.maxSell);
        autoTradeBox.style.border = "none";
      },
      error: function (result) {
        alert("Max-auto Error");
      },
    });
  } else if (!$("#select-trade").val()) {
    autoTradeBox.style.border = "1px solid red";
    return "No Input";
  }
});

// var binanceSocketLivePrice = new WebSocket(
//   "wss://stream.binance.com:9443/ws/btcusdt@ticker"
// );

// tradeSymbols = ["btcusdt", "btceur", "eurusdt"];

// var priceSocket_BTCUSDT = new WebSocket(
//   "wss://stream.binance.com:9443/ws/BTCUSDT@ticker"
// );
// var priceSocket_BTCEUR = new WebSocket(
//   "wss://stream.binance.com:9443/ws/BTCEUR@ticker"
// );
// var priceSocket_EURUSDT = new WebSocket(
//   "wss://stream.binance.com:9443/ws/EURUSDT@ticker"
// );

// Partly determines default price ticker
// document.getElementById("select-trade").addEventListener("change", function () {
//   livePriceSocket = eval(`priceSocket_${this.value}`);

// fetch(`http://localhost:5000/${this.value}_candles`)
//   .then((r) => r.json())
//   .then((response) => {
//     response.pop();
//     console.log(response);
//     candleSeries.setData(response);
//   });

$("#select-trade").change(function (event) {
  event.preventDefault();
  // console.log(event.target.id);
  // console.log(this.value);
  loader.style.display = "block";

  socket.removeEventListener("message", updateCandles);
  priceSocket.removeEventListener("message", updatePriceTicker);

  let currentSymbol = this.value.toLowerCase();
  priceSocket = eval(`priceSocket_${currentSymbol}`);

  let candleSize;

  for (let x = 0; x < candleSelectors.length; x++) {
    if (candleSelectors[x].value) {
      candleSize = candleSelectors[x].value;
      // console.log(candleSize);
    }
  }

  socket = eval(`binanceSocket_${currentSymbol}_${candleSize}`);

  // console.log(this.value);
  // console.log($("#select-trade").val());
  $.ajax({
    url: "/generate_candles",
    type: "POST",
    data: {
      tradeSymbol: currentSymbol,
      candleSize: candleSize,
    },
    success: function (result) {
      // var data = JSON.parse(result);
      // console.log(result);
      // wipe
      $("input.input-price").val("");
      $("input.input-amount").val("");
      if (currentSymbol === "eurusdt") {
        candleSeries.applyOptions({
          priceFormat: {
            type: "price",
            precision: 4,
            minMove: 0.0001,
          },
        });
      } else {
        candleSeries.applyOptions({
          priceFormat: {
            type: "price",
            precision: 0,
            minMove: 1,
          },
        });
      }
      result.pop();
      candleSeries.setData(result);
      loader.style.display = "none";
      let baseA = currentSymbol.substring(0, 3);
      let quoteA = currentSymbol.substring(3);
      $("span.base-asset").html(baseA.toUpperCase());
      $("span.quote-asset").html(quoteA.toUpperCase());
      // $("span.asset-placeholder.base-asset").html(baseA.toUpperCase());
      socket.addEventListener("message", updateCandles);
      priceSocket.addEventListener("message", updatePriceTicker);
      // console.log(result.msg);
    },
    error: function (result) {
      alert("error");
    },
  });
});

// });
