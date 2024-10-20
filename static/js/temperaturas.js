function handleRadioChange() {
    input_fahrenheit = document.getElementById("input_fahrenheit");
    input_celsius = document.getElementById("input_celsius");
    check_Celsius = document.getElementById("check_Celsius");
    check_Fahrenheit = document.getElementById("check_Fahrenheit");

    if (check_Celsius.checked) {
        input_fahrenheit.disabled = false;
        input_celsius.disabled = true;
    } else if (check_Fahrenheit.checked) {
        input_celsius.disabled = false;
        input_fahrenheit.disabled = true;
    }
}

window.onload = function() {
    var radios = document.querySelectorAll('input[type=radio][name="conversion"]');
    radios.forEach(function(radio) {
        radio.addEventListener('change', handleRadioChange);
    });
    handleRadioChange(); // Para configurar el estado inicial
};