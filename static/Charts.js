var chart = LightweightCharts.createChart(document.getElementById("charts"), {
  width: 1060,
  height: 537,
  layout: {
    backgroundColor: "#161616",
    textColor: "rgba(255, 255, 255, 0.9)",
    fontSize: 15,
    fontFamily: "Ubuntu",
    // backgroundColor: "#FAEBD7",
    // textColor: "#696969",
  },
  grid: {
    vertLines: {
      color: "#424242",
      width: 0.3,
    },
    horzLines: {
      color: "#424242",
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

// if (window.location.href === "http://localhost:5000/") {
fetch("http://localhost:5000/default")
  .then((r) => r.json())
  .then((response) => {
    response.pop();
    candleSeries.setData(response);
  });
// }

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

for (let i = 0; i < candles.length; i++) {
  eval(
    `var binanceSocket_${candles[i]} = new WebSocket("wss://stream.binance.com:9443/ws/btcusdt@kline_${candles[i]}");`
  );
}

// Partyle determines default candlestick size
var socket = binanceSocket_4h;

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
    socket = eval(`binanceSocket_${this.value}`);
    event.preventDefault();
    console.log(this.value);
    $.ajax({
      url: "/generate_candles",
      type: "POST",
      data: {
        tradeSymbol: $("#select-trade").val(),
        candleSize: this.value,
      },
      success: function (result) {
        result.json().then((data) => {
          console.log(data);
          data.pop();
          candleSeries.setData(data);
        });
        // console.log(result.msg);
      },
      error: function (result) {
        alert("error");
      },
    });
  });

  socket.removeEventListener("message", updateCandles);
  socket.addEventListener("message", updateCandles);
}

// document
//   .getElementById("select-minute-candles")
//   .addEventListener("change", function () {
//     // console.log(this.value);
//     socket = eval(`binanceSocket_${this.value}`);
//     // console.log(socket);
//     fetch(`http://localhost:5000/${this.value}_candles`)
//       .then((r) => r.json())
//       .then((response) => {
//         response.pop();
//         console.log(response);
//         candleSeries.setData(response);
//       });
//     socket.removeEventListener("message", updateCandles);
//     socket.addEventListener("message", updateCandles);
//   });

// document
//   .getElementById("select-hour-candles")
//   .addEventListener("change", function () {
//     // console.log(this.value);
//     socket = eval(`binanceSocket_${this.value}`);
//     // console.log(socket);
//     fetch(`http://localhost:5000/${this.value}_candles`)
//       .then((r) => r.json())
//       .then((response) => {
//         response.pop();
//         console.log(response);
//         candleSeries.setData(response);
//       });
//     socket.removeEventListener("message", updateCandles);
//     socket.addEventListener("message", updateCandles);
//   });

// document
//   .getElementById("select-day-candles")
//   .addEventListener("change", function () {
//     // console.log(this.value);
//     socket = eval(`binanceSocket_${this.value}`);
//     // console.log(socket);
//     fetch(`http://localhost:5000/${this.value}_candles`)
//       .then((r) => r.json())
//       .then((response) => {
//         response.pop();
//         candleSeries.setData(response);
//       });
//     socket.removeEventListener("message", updateCandles);
//     socket.addEventListener("message", updateCandles);
//   });

var x = 0;
function updateCandles(e) {
  let message = JSON.parse(e.data);
  // console.log(socket);
  for (; x < 1; x++) {
    console.log(message);
  }
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
socket.addEventListener("message", updateCandles);

document.getElementById("reset-chart-icon").onclick = function (event) {
  chart.timeScale().scrollToRealTime(3);
  // chart.timeScale().resetTimeScale();
};
