$(document).ready(function() {
    alert($('#handler').val());

    $('#tabledata1').DataTable();
    $('#tabledata2').DataTable();
    
    $('.menu .item').tab();

    age = $('#age').val()
    
    if (age < 14) {
        $('#id_record-0-vaccine').prop('disabled', 'disabled');
        $('#id_record-0-date_vaccinated').prop('disabled', 'disabled');
        $('#id_record-0-image').prop('disabled', 'disabled');
    }
    if (age < 28) {
        $('#id_record-1-vaccine').prop('disabled', 'disabled');
        $('#id_record-1-date_vaccinated').prop('disabled', 'disabled');
        $('#id_record-1-image').prop('disabled', 'disabled');
    }
    if (age < 42) {
        $('#id_record-2-vaccine').prop('disabled', 'disabled');
        $('#id_record-2-date_vaccinated').prop('disabled', 'disabled');
        $('#id_record-2-image').prop('disabled', 'disabled');

        $('#id_record-3-vaccine').prop('disabled', 'disabled');
        $('#id_record-3-date_vaccinated').prop('disabled', 'disabled');
        $('#id_record-3-image').prop('disabled', 'disabled');

        $('#id_record-4-vaccine').prop('disabled', 'disabled');
        $('#id_record-4-date_vaccinated').prop('disabled', 'disabled');
        $('#id_record-4-image').prop('disabled', 'disabled');
    }
    if (age < 56) {
        $('#id_record-5-vaccine').prop('disabled', 'disabled');
        $('#id_record-5-date_vaccinated').prop('disabled', 'disabled');
        $('#id_record-5-image').prop('disabled', 'disabled');

        $('#id_record-6-vaccine').prop('disabled', 'disabled');
        $('#id_record-6-date_vaccinated').prop('disabled', 'disabled');
        $('#id_record-6-image').prop('disabled', 'disabled');
    }
    if (age < 63) {
        $('#id_record-7-vaccine').prop('disabled', 'disabled');
        $('#id_record-7-date_vaccinated').prop('disabled', 'disabled');
        $('#id_record-7-image').prop('disabled', 'disabled');

        $('#id_record-8-vaccine').prop('disabled', 'disabled');
        $('#id_record-8-date_vaccinated').prop('disabled', 'disabled');
        $('#id_record-8-image').prop('disabled', 'disabled');
    }
    if (age < 70) {
        $('#id_record-9-vaccine').prop('disabled', 'disabled');
        $('#id_record-9-date_vaccinated').prop('disabled', 'disabled');
        $('#id_record-9-image').prop('disabled', 'disabled');
    }
    if (age < 77) {
        $('#id_record-10-vaccine').prop('disabled', 'disabled');
        $('#id_record-10-date_vaccinated').prop('disabled', 'disabled');
        $('#id_record-10-image').prop('disabled', 'disabled');
    }
    if (age < 84) {
        $('#id_record-11-vaccine').prop('disabled', 'disabled');
        $('#id_record-11-date_vaccinated').prop('disabled', 'disabled');
        $('#id_record-11-image').prop('disabled', 'disabled');

        $('#id_record-12-vaccine').prop('disabled', 'disabled');
        $('#id_record-12-date_vaccinated').prop('disabled', 'disabled');
        $('#id_record-12-image').prop('disabled', 'disabled');

        $('#id_record-13-vaccine').prop('disabled', 'disabled');
        $('#id_record-13-date_vaccinated').prop('disabled', 'disabled');
        $('#id_record-13-image').prop('disabled', 'disabled');
    }
    if (age < 98) {
        $('#id_record-14-vaccine').prop('disabled', 'disabled');
        $('#id_record-14-date_vaccinated').prop('disabled', 'disabled');
        $('#id_record-14-image').prop('disabled', 'disabled');
    }
    if (age < 105) {
        $('#id_record-15-vaccine').prop('disabled', 'disabled');
        $('#id_record-15-date_vaccinated').prop('disabled', 'disabled');
        $('#id_record-15-image').prop('disabled', 'disabled');
    }
    if (age < 112) {
        $('#id_record-16-vaccine').prop('disabled', 'disabled');
        $('#id_record-16-date_vaccinated').prop('disabled', 'disabled');
        $('#id_record-16-image').prop('disabled', 'disabled');
    }
    if (age < 126) {
        $('#id_record-17-vaccine').prop('disabled', 'disabled');
        $('#id_record-17-date_vaccinated').prop('disabled', 'disabled');
        $('#id_record-17-image').prop('disabled', 'disabled');

        $('#id_record-18-vaccine').prop('disabled', 'disabled');
        $('#id_record-18-date_vaccinated').prop('disabled', 'disabled');
        $('#id_record-18-image').prop('disabled', 'disabled');
    }
    if (age < 140) {
        $('#id_record-19-vaccine').prop('disabled', 'disabled');
        $('#id_record-19-date_vaccinated').prop('disabled', 'disabled');
        $('#id_record-19-image').prop('disabled', 'disabled');
    }
    if (age < 154) {
        $('#id_record-20-vaccine').prop('disabled', 'disabled');
        $('#id_record-20-date_vaccinated').prop('disabled', 'disabled');
        $('#id_record-20-image').prop('disabled', 'disabled');
    }
    if (age < 168) {
        $('#id_record-21-vaccine').prop('disabled', 'disabled');
        $('#id_record-21-date_vaccinated').prop('disabled', 'disabled');
        $('#id_record-21-image').prop('disabled', 'disabled');
    }
    if (age < 182) {
        $('#id_record-22-vaccine').prop('disabled', 'disabled');
        $('#id_record-22-date_vaccinated').prop('disabled', 'disabled');
        $('#id_record-22-image').prop('disabled', 'disabled');
    }
    if (age < 196) {
        $('#id_record-23-vaccine').prop('disabled', 'disabled');
        $('#id_record-23-date_vaccinated').prop('disabled', 'disabled');
        $('#id_record-23-image').prop('disabled', 'disabled');
    }
    if (age < 210) {
        $('#id_record-24-vaccine').prop('disabled', 'disabled');
        $('#id_record-24-date_vaccinated').prop('disabled', 'disabled');
        $('#id_record-24-image').prop('disabled', 'disabled');
    }
    if (age < 224) {
        $('#id_record-25-vaccine').prop('disabled', 'disabled');
        $('#id_record-25-date_vaccinated').prop('disabled', 'disabled');
        $('#id_record-25-image').prop('disabled', 'disabled');
    }
    if (age < 238) {
        $('#id_record-26-vaccine').prop('disabled', 'disabled');
        $('#id_record-26-date_vaccinated').prop('disabled', 'disabled');
        $('#id_record-26-image').prop('disabled', 'disabled');
    }

});