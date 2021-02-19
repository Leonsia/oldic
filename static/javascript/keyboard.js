let keys = document.getElementsByClassName('btn-key');
let display = document.getElementById('display');
for (let key of keys) {
  key.onclick = function () {
  display.value = display.value + key.textContent;
  display.focus();
  }
};
