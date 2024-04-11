// DECLARATION OF GENERAL VARIABLES
let success_messages = {
    "1": "Version mise à jour avec succès",
    "2": "Version ajoutée avec succès",
    "3": "Projet ajouté avec succès"
}
let searchParams = new URLSearchParams(window.location.search)

// DECLARATION OF GENERAL FUNCTIONS
function getCookie(c_name)
{
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
 }

// CODE TO RUN IN EVERY PAGE
$( function() {
    $( "#id_date_of_release" ).datepicker();
} );

if (searchParams.has('message_success'))
{
    message_success = searchParams.get('message_success')
    Swal.fire({
        position: 'center-center',
        icon: 'success',
        title: success_messages[message_success],
        showConfirmButton: false,
        timer: 1500
      })
}



