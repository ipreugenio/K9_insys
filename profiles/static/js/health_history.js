$(document).ready(function() {
    $('#tabledata1').DataTable();
    $('#tabledata2').DataTable({
    "order": [[ 0, "desc" ]]
    });
    $('#tabledata3').DataTable();
    $('.menu .item').tab();

    // disabled all vaccine used initial
    $('#s_deworming_1').prop('disabled', 'disabled');
    $('#s_deworming_2').prop('disabled', 'disabled');
    $('#s_deworming_3').prop('disabled', 'disabled');
    $('#s_dhppil_cv_1').prop('disabled', 'disabled');
    $('#s_heartworm_1').prop('disabled', 'disabled');
    $('#s_bordetella_1').prop('disabled', 'disabled');
    $('#s_tick_flea_1').prop('disabled', 'disabled');
    $('#s_dhppil_cv_2').prop('disabled', 'disabled');
    $('#s_deworming_4').prop('disabled', 'disabled');
    $('#s_heartworm_2').prop('disabled', 'disabled');
    $('#s_bordetella_2').prop('disabled', 'disabled');
    $('#s_anti_rabies').prop('disabled', 'disabled');
    $('#s_tick_flea_2').prop('disabled', 'disabled');
    $('#s_dhppil_cv_3').prop('disabled', 'disabled');
    $('#s_heartworm_3').prop('disabled', 'disabled');
    $('#s_dhppil4_1').prop('disabled', 'disabled');
    $('#s_tick_flea_3').prop('disabled', 'disabled');
    $('#s_dhppil4_2').prop('disabled', 'disabled');
    $('#s_heartworm_4').prop('disabled', 'disabled');
    $('#s_tick_flea_4').prop('disabled', 'disabled');
    $('#s_heartworm_5').prop('disabled', 'disabled');
    $('#s_tick_flea_5').prop('disabled', 'disabled');
    $('#s_heartworm_6').prop('disabled', 'disabled');
    $('#s_tick_flea_6').prop('disabled', 'disabled');
    $('#s_heartworm_7').prop('disabled', 'disabled');
    $('#s_tick_flea_7').prop('disabled', 'disabled');
    $('#s_heartworm_8').prop('disabled', 'disabled');

    // if checkbox is checked -> vaccine is enabled
    // else if checkbox is not checked -> vaccine is disabled

    $("input[name='s_deworming_1']").change(function() {   
        if ($('#dog_days').val() < 14){
            alert('K9 is less than 2 weeks')
            $("input[name='deworming_1']").prop('checked', false)
            $('#s_deworming_1').prop('disabled', 'disabled');
        }
        
        if ($("input[name='deworming_1']").is(':checked')){
            $('#s_deworming_1').prop('disabled', false);
        }else{
            $('#s_deworming_1').prop('disabled', 'disabled');
        }
    });

    $("input[name='deworming_2']").change(function() {   
        if ($('#dog_days').val() < 28){
            alert('K9 is less than 4 weeks')
            $("input[name='deworming_2']").prop('checked', false)
            $('#s_deworming_2').prop('disabled', 'disabled');
        }
        
        if ($("input[name='deworming_2']").is(':checked')){
            $('#s_deworming_2').prop('disabled', false);
        }else{
            $('#s_deworming_2').prop('disabled', 'disabled');
        }
    });

    $("input[name='deworming_3']").change(function() {   
        if ($('#dog_days').val() < 42){
            alert('K9 is less than 6 weeks')
            $("input[name='deworming_3']").prop('checked', false)
            $('#s_deworming_3').prop('disabled', 'disabled');
        }
        if ($("input[name='deworming_3']").is(':checked')){
            $('#s_deworming_3').prop('disabled', false);
        }else{
            $('#s_deworming_3').prop('disabled', 'disabled');
        }
    });

    $("input[name='dhppil_cv_1']").change(function() {   
        if ($('#dog_days').val() < 42){
            alert('K9 is less than 6 weeks')
            $("input[name='dhppil_cv_1']").prop('checked', false)
            $('#s_dhppil_cv_1').prop('disabled', 'disabled');
        }
        if ($("input[name='dhppil_cv_1']").is(':checked')){
            $('#s_dhppil_cv_1').prop('disabled', false);
        }else{
            $('#s_dhppil_cv_1').prop('disabled', 'disabled');
        }
    });

    $("input[name='heartworm_1']").change(function() {   
        if ($('#dog_days').val() < 42){
            alert('K9 is less than 6 weeks')
            $("input[name='heartworm_1']").prop('checked', false)
            $('#s_heartworm_1').prop('disabled', 'disabled');
        }
        if ($("input[name='heartworm_1']").is(':checked')){
            $('#s_heartworm_1').prop('disabled', false);
        }else{
            $('#s_heartworm_1').prop('disabled', 'disabled');
        }
    });

    $("input[name='bordetella_1']").change(function() {   
        if ($('#dog_days').val() < 56){
            alert('K9 is less than 8 weeks')
            $("input[name='bordetella_1']").prop('checked', false)
            $('#s_bordetella_1').prop('disabled', 'disabled');
        }
        if ($("input[name='bordetella_1']").is(':checked')){
            $('#s_bordetella_1').prop('disabled', false);
        }else{
            $('#s_bordetella_1').prop('disabled', 'disabled');
        }
    });

    $("input[name='tick_flea_1']").change(function() {  
        if ($('#dog_days').val() < 56){
            alert('K9 is less than 8 weeks')
            $("input[name='tick_flea_1']").prop('checked', false)
            $('#s_tick_flea_1').prop('disabled', 'disabled');
        } 
        if ($("input[name='tick_flea_1']").is(':checked')){
            $('#s_tick_flea_1').prop('disabled', false);
        }else{
            $('#s_tick_flea_1').prop('disabled', 'disabled');
        }
    });

    $("input[name='dhppil_cv_2']").change(function() {  
        if ($('#dog_days').val() < 63){
            alert('K9 is less than 9 weeks')
            $("input[name='dhppil_cv_2']").prop('checked', false)
            $('#s_dhppil_cv_2').prop('disabled', 'disabled');
        }  
        if ($("input[name='dhppil_cv_2']").is(':checked')){
            $('#s_dhppil_cv_2').prop('disabled', false);
        }else{
            $('#s_dhppil_cv_2').prop('disabled', 'disabled');
        }
    });

    $("input[name='deworming_4']").change(function() {  
        if ($('#dog_days').val() < 63){
            alert('K9 is less than 9 weeks')
            $("input[name='deworming_4']").prop('checked', false)
            $('#s_deworming_4').prop('disabled', 'disabled');
        }  
        if ($("input[name='deworming_4']").is(':checked')){
            $('#s_deworming_4').prop('disabled', false);
        }else{
            $('#s_deworming_4').prop('disabled', 'disabled');
        }
    });

    $("input[name='heartworm_2']").change(function() {   
        if ($('#dog_days').val() < 70){
            alert('K9 is less than 10 weeks')
            $("input[name='heartworm_2']").prop('checked', false)
            $('#s_heartworm_2').prop('disabled', 'disabled');
        }  
        if ($("input[name='heartworm_2']").is(':checked')){
            $('#s_heartworm_2').prop('disabled', false);
        }else{
            $('#s_heartworm_2').prop('disabled', 'disabled');
        }
    });

    $("input[name='bordetella_2']").change(function() {   
        if ($('#dog_days').val() < 77){
            alert('K9 is less than 11 weeks')
            $("input[name='bordetella_2']").prop('checked', false)
            $('#s_bordetella_2').prop('disabled', 'disabled');
        }  
        if ($("input[name='bordetella_2']").is(':checked')){
            $('#s_bordetella_2').prop('disabled', false);
        }else{
            $('#s_bordetella_2').prop('disabled', 'disabled');
        }
    });

    $("input[name='tick_flea_2']").change(function() {  
        if ($('#dog_days').val() < 84){
            alert('K9 is less than 12 weeks')
            $("input[name='tick_flea_2']").prop('checked', false)
            $('#s_tick_flea_2').prop('disabled', 'disabled');
        }   
        if ($("input[name='tick_flea_2']").is(':checked')){
            $('#s_tick_flea_2').prop('disabled', false);
        }else{
            $('#s_tick_flea_2').prop('disabled', 'disabled');
        }
    });

    $("input[name='anti_rabies']").change(function() {  
        if ($('#dog_days').val() < 84){
            alert('K9 is less than 12 weeks')
            $("input[name='anti_rabies']").prop('checked', false)
            $('#s_anti_rabies').prop('disabled', 'disabled');
        }    
        if ($("input[name='anti_rabies']").is(':checked')){
            $('#s_anti_rabies').prop('disabled', false);
        }else{
            $('#s_anti_rabies').prop('disabled', 'disabled');
        }
    });

    $("input[name='dhppil_cv_3']").change(function() { 
        if ($('#dog_days').val() < 84){
            alert('K9 is less than 12 weeks')
            $("input[name='dhppil_cv_3']").prop('checked', false)
            $('#s_dhppil_cv_3').prop('disabled', 'disabled');
        }     
        if ($("input[name='dhppil_cv_3']").is(':checked')){
            $('#s_dhppil_cv_3').prop('disabled', false);
        }else{
            $('#s_dhppil_cv_3').prop('disabled', 'disabled');
        }
    });

    $("input[name='heartworm_3']").change(function() {  
        if ($('#dog_days').val() < 98){
            alert('K9 is less than 14 weeks')
            $("input[name='heartworm_3']").prop('checked', false)
            $('#s_heartworm_3').prop('disabled', 'disabled');
        }      
        if ($("input[name='heartworm_3']").is(':checked')){
            $('#s_heartworm_3').prop('disabled', false);
        }else{
            $('#s_heartworm_3').prop('disabled', 'disabled');
        }
    });

    $("input[name='dhppil4_1']").change(function() {   
        if ($('#dog_days').val() < 105){
            alert('K9 is less than 15 weeks')
            $("input[name='dhppil4_1']").prop('checked', false)
            $('#s_dhppil4_1').prop('disabled', 'disabled');
        }     
        if ($("input[name='dhppil4_1']").is(':checked')){
            $('#s_dhppil4_1').prop('disabled', false);
        }else{
            $('#s_dhppil4_1').prop('disabled', 'disabled');
        }
    });

    $("input[name='tick_flea_3']").change(function() {   
        if ($('#dog_days').val() < 112){
            alert('K9 is less than 16 weeks')
            $("input[name='tick_flea_3']").prop('checked', false)
            $('#s_tick_flea_3').prop('disabled', 'disabled');
        }     
        if ($("input[name='tick_flea_3']").is(':checked')){
            $('#s_tick_flea_3').prop('disabled', false);
        }else{
            $('#s_tick_flea_3').prop('disabled', 'disabled');
        }
    });

    $("input[name='dhppil4_2']").change(function() {   
        if ($('#dog_days').val() < 126){
            alert('K9 is less than 18 weeks')
            $("input[name='dhppil4_2']").prop('checked', false)
            $('#s_dhppil4_2').prop('disabled', 'disabled');
        }     
        if ($("input[name='dhppil4_2']").is(':checked')){
            $('#s_dhppil4_2').prop('disabled', false);
        }else{
            $('#s_dhppil4_2').prop('disabled', 'disabled');
        }
    });

    $("input[name='heartworm_4']").change(function() {   
        if ($('#dog_days').val() < 126){
            alert('K9 is less than 18 weeks')
            $("input[name='heartworm_4']").prop('checked', false)
            $('#s_heartworm_4').prop('disabled', 'disabled');
        }     
        if ($("input[name='heartworm_4']").is(':checked')){
            $('#s_heartworm_4').prop('disabled', false);
        }else{
            $('#s_heartworm_4').prop('disabled', 'disabled');
        }
    });

    $("input[name='tick_flea_4']").change(function() {   
        if ($('#dog_days').val() < 140){
            alert('K9 is less than 20 weeks')
            $("input[name='tick_flea_4']").prop('checked', false)
            $('#s_tick_flea_4').prop('disabled', 'disabled');
        }    
        if ($("input[name='tick_flea_4']").is(':checked')){
            $('#s_tick_flea_4').prop('disabled', false);
        }else{
            $('#s_tick_flea_4').prop('disabled', 'disabled');
        }
    });

    $("input[name='heartworm_5']").change(function() {   
        if ($('#dog_days').val() < 154){
            alert('K9 is less than 22 weeks')
            $("input[name='heartworm_5']").prop('checked', false)
            $('#s_heartworm_5').prop('disabled', 'disabled');
        }    
        if ($("input[name='heartworm_5']").is(':checked')){
            $('#s_heartworm_5').prop('disabled', false);
        }else{
            $('#s_heartworm_5').prop('disabled', 'disabled');
        }
    });

    $("input[name='tick_flea_5']").change(function() {   
        if ($('#dog_days').val() < 168){
            alert('K9 is less than 24 weeks')
            $("input[name='tick_flea_5']").prop('checked', false)
            $('#s_tick_flea_5').prop('disabled', 'disabled');
        }    
        if ($("input[name='tick_flea_5']").is(':checked')){
            $('#s_tick_flea_5').prop('disabled', false);
        }else{
            $('#s_tick_flea_5').prop('disabled', 'disabled');
        }
    });

    $("input[name='heartworm_6']").change(function() { 
        if ($('#dog_days').val() < 183){
            alert('K9 is less than 26 weeks')
            $("input[name='heartworm_6']").prop('checked', false)
            $('#s_heartworm_6').prop('disabled', 'disabled');
        }      
        if ($("input[name='heartworm_6']").is(':checked')){
            $('#s_heartworm_6').prop('disabled', false);
        }else{
            $('#s_heartworm_6').prop('disabled', 'disabled');
        }
    });

    $("input[name='tick_flea_6']").change(function() {   
        if ($('#dog_days').val() < 196){
            alert('K9 is less than 28 weeks')
            $("input[name='tick_flea_6']").prop('checked', false)
            $('#s_tick_flea_6').prop('disabled', 'disabled');
        }      
        if ($("input[name='tick_flea_6']").is(':checked')){
            $('#s_tick_flea_6').prop('disabled', false);
        }else{
            $('#s_tick_flea_6').prop('disabled', 'disabled');
        }
    });

    $("input[name='heartworm_7']").change(function() { 
        if ($('#dog_days').val() < 210){
            alert('K9 is less than 30 weeks')
            $("input[name='heartworm_7']").prop('checked', false)
            $('#s_heartworm_7').prop('disabled', 'disabled');
        }        
        if ($("input[name='heartworm_7']").is(':checked')){
            $('#s_heartworm_7').prop('disabled', false);
        }else{
            $('#s_heartworm_7').prop('disabled', 'disabled');
        }
    });

    $("input[name='tick_flea_7']").change(function() { 
        if ($('#dog_days').val() < 224){
            alert('K9 is less than 32 weeks')
            $("input[name='tick_flea_7']").prop('checked', false)
            $('#s_tick_flea_7').prop('disabled', 'disabled');
        }      
        if ($("input[name='tick_flea_7']").is(':checked')){
            $('#s_tick_flea_7').prop('disabled', false);
        }else{
            $('#s_tick_flea_7').prop('disabled', 'disabled');
        }
    });

    $("input[name='heartworm_8']").change(function() { 
        if ($('#dog_days').val() < 238){
            alert('K9 is less than 34 weeks')
            $("input[name='heartworm_8']").prop('checked', false)
            $('#s_heartworm_8').prop('disabled', 'disabled');
        }        
        if ($("input[name='heartworm_8']").is(':checked')){
            $('#s_heartworm_8').prop('disabled', false);
        }else{
            $('#s_heartworm_8').prop('disabled', 'disabled');
        }
    });

    //if checkbox and vaccine used is checked  
    if ($("input[name='deworming_1']").is(':checked') && $("input[name='deworming_1']").val() != ''){
        $('#s_deworming_1').prop('disabled', true);
        $("input[name='deworming_1']").prop('disabled', true);
    }   
    
    if ($("input[name='deworming_2']").is(':checked') && $("input[name='deworming_2']").val() != ''){
        $('#s_deworming_2').prop('disabled', true);
        $("input[name='deworming_2']").prop('disabled', true);
    }   

    if ($("input[name='deworming_3']").is(':checked') && $("input[name='deworming_3']").val() != ''){
        $('#s_deworming_3').prop('disabled', true);
        $("input[name='deworming_3']").prop('disabled', true);
    }   

    if ($("input[name='dhppil_cv_1']").is(':checked') && $("input[name='dhppil_cv_1']").val() != ''){
        $('#s_dhppil_cv_1').prop('disabled', true);
        $("input[name='dhppil_cv_1']").prop('disabled', true);
    }   

    if ($("input[name='heartworm_1']").is(':checked') && $("input[name='heartworm_1']").val() != ''){
        $('#s_heartworm_1').prop('disabled', true);
        $("input[name='heartworm_1']").prop('disabled', true);
    }   

    if ($("input[name='bordetella_1']").is(':checked') && $("input[name='bordetella_1']").val() != ''){
        $('#s_bordetella_1').prop('disabled', true);
        $("input[name='bordetella_1']").prop('disabled', true);
    }   

    if ($("input[name='tick_flea_1']").is(':checked') && $("input[name='tick_flea_1']").val() != ''){
        $('#s_tick_flea_1').prop('disabled', true);
        $("input[name='tick_flea_1']").prop('disabled', true);
    }   

    if ($("input[name='dhppil_cv_2']").is(':checked') && $("input[name='dhppil_cv_2']").val() != ''){
        $('#s_dhppil_cv_2').prop('disabled', true);
        $("input[name='dhppil_cv_2']").prop('disabled', true);
    }   

    if ($("input[name='deworming_4']").is(':checked') && $("input[name='deworming_4']").val() != ''){
        $('#s_deworming_4').prop('disabled', true);
        $("input[name='deworming_4']").prop('disabled', true);
    }   

    if ($("input[name='heartworm_2']").is(':checked') && $("input[name='heartworm_2']").val() != ''){
        $('#s_heartworm_2').prop('disabled', true);
        $("input[name='heartworm_2']").prop('disabled', true);
    }   

    if ($("input[name='bordetella_2']").is(':checked') && $("input[name='bordetella_2']").val() != ''){
        $('#s_bordetella_2').prop('disabled', true);
        $("input[name='bordetella_2']").prop('disabled', true);
    }   

    if ($("input[name='anti_rabies']").is(':checked') && $("input[name='anti_rabies']").val() != ''){
        $('#s_anti_rabies').prop('disabled', true);
        $("input[name='anti_rabies']").prop('disabled', true);
    }   

    if ($("input[name='tick_flea_2']").is(':checked') && $("input[name='tick_flea_2']").val() != ''){
        $('#tick_flea_2').prop('disabled', true);
        $("input[name='tick_flea_2']").prop('disabled', true);
    }   

    if ($("input[name='dhppil_cv_3']").is(':checked') && $("input[name='dhppil_cv_3']").val() != ''){
        $('#s_dhppil_cv_3').prop('disabled', true);
        $("input[name='dhppil_cv_3']").prop('disabled', true);
    }   

    if ($("input[name='heartworm_3']").is(':checked') && $("input[name='heartworm_3']").val() != ''){
        $('#s_heartworm_3').prop('disabled', true);
        $("input[name='heartworm_3']").prop('disabled', true);
    }   

    if ($("input[name='dhppil4_1']").is(':checked') && $("input[name='dhppil4_1']").val() != ''){
        $('#s_dhppil4_1').prop('disabled', true);
        $("input[name='dhppil4_1']").prop('disabled', true);
    }   

    if ($("input[name='tick_flea_3']").is(':checked') && $("input[name='tick_flea_3']").val() != ''){
        $('#s_tick_flea_3').prop('disabled', true);
        $("input[name='tick_flea_3']").prop('disabled', true);
    }   

    if ($("input[name='dhppil4_2']").is(':checked') && $("input[name='dhppil4_2']").val() != ''){
        $('#s_dhppil4_2').prop('disabled', true);
        $("input[name='dhppil4_2']").prop('disabled', true);
    }   
    
    if ($("input[name='heartworm_4']").is(':checked') && $("input[name='heartworm_4']").val() != ''){
        $('#s_heartworm_4').prop('disabled', true);
        $("input[name='heartworm_4']").prop('disabled', true);
    }   

    if ($("input[name='tick_flea_4']").is(':checked') && $("input[name='tick_flea_4']").val() != ''){
        $('#s_tick_flea_4').prop('disabled', true);
        $("input[name='tick_flea_4']").prop('disabled', true);
    }   

    if ($("input[name='heartworm_5']").is(':checked') && $("input[name='heartworm_5']").val() != ''){
        $('#s_heartworm_5').prop('disabled', true);
        $("input[name='heartworm_5']").prop('disabled', true);
    }   
    
    if ($("input[name='tick_flea_5']").is(':checked') && $("input[name='tick_flea_5']").val() != ''){
        $('#s_tick_flea_5').prop('disabled', true);
        $("input[name='tick_flea_5']").prop('disabled', true);
    }   

    if ($("input[name='heartworm_6']").is(':checked') && $("input[name='heartworm_6']").val() != ''){
        $('#s_heartworm_6').prop('disabled', true);
        $("input[name='heartworm_6']").prop('disabled', true);
    }   
    
    if ($("input[name='tick_flea_6']").is(':checked') && $("input[name='tick_flea_6']").val() != ''){
        $('#s_tick_flea_6').prop('disabled', true);
        $("input[name='tick_flea_6']").prop('disabled', true);
    }   

    if ($("input[name='heartworm_7']").is(':checked') && $("input[name='heartworm_7']").val() != ''){
        $('#s_heartworm_7').prop('disabled', true);
        $("input[name='heartworm_7']").prop('disabled', true);
    }   

    if ($("input[name='tick_flea_7']").is(':checked') && $("input[name='tick_flea_7']").val() != ''){
        $('#s_tick_flea_7').prop('disabled', true);
        $("input[name='tick_flea_7']").prop('disabled', true);
    }   

    if ($("input[name='heartworm_8']").is(':checked') && $("input[name='heartworm_8']").val() != ''){
        $('#s_heartworm_8').prop('disabled', true);
        $("input[name='heartworm_8']").prop('disabled', true);
    }   
});
