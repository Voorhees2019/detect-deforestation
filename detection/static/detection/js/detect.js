// Place fileName to input file label after successfully uploaded file
(function () {
    'use strict';
    $('.input-file').each(function () {
        let $input = $(this),
            $label = $input.next('.js-labelFile'),
            labelVal = $label.html();

        $input.on('change', function (element) {
            let fileName = '';
            if (element.target.value) fileName = element.target.value.split('\\').pop();
            fileName ? $label.addClass('has-file').find('.js-fileName').html(fileName) : $label.removeClass('has-file').html(labelVal);
        });
    });

})();

function checkUploadedFile() {
    if (document.getElementById("uploadedFile").files.length === 0) {
        alert('Please attach a photo');
    }
}
