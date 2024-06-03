$(document).ready(function() {
    $('#imageUpload').change(function() {
        const file = this.files[0];
        if (file) {
            let reader = new FileReader();
            reader.onload = function(event) {
                $('#imagePreview').attr('src', event.target.result);
                $('.image-section').show();  // Show image and predict button once image is chosen
            };
            reader.readAsDataURL(file);
        }
    });

    $('#btn-predict').click(function() {
        let formData = new FormData($('#upload-file')[0]);
        formData.append('file', $('#imageUpload')[0].files[0]);

        $.ajax({
            type: 'POST',
            url: '/predict',
            data: formData,
            processData: false,
            contentType: false,
            beforeSend: function() {
                $('.loader').show();
                $('.result-section').hide();  // Hide previous results
            },
            success: function(data) {
                $('.result-section').show();
                $('#result span').html(data);
                $('#description').html(getDescription(data));  // Display the description based on the result
            },
            complete: function() {
                $('.loader').hide();
            }
        });
    });
});

function getDescription(result) {
    switch (result) {
        case "Choroidal neovascularization (CNV)":
            return "Choroidal Neovascularization involves growth of new, abnormal blood vessels under the retina and the macula.<br> This is typically caused by the body's response to impaired blood flow, leading to further damage and loss of vision if untreated.";
        case "Diabetic macular edema (DME)":
            return "Diabetic Macular Edema is a complication of diabetes characterized by swelling in the retina due to leaking vessels, which can cause vision impairment if not properly managed";
        case "Drusen":
            return "Drusen are yellow deposits beneath the retina commonly linked to aging. <br> While typically not causing vision loss directly, an increase in their size or quantity can heighten the risk of vision problems.";
        case "Normal":
            return "The scan shows a healthy retina with no pathological changes.";
        default:
            return "Unknown condition. Please consult an eye care professional.";
    }
}
