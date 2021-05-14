const date = new Date();
document.querySelector('.year').innerHTML = date.getFullYear();

setTimeout(function () {
    $('.alert').alert('close');
}, 3000);
