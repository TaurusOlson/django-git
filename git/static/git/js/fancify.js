$(document).ready(function() {

    // Toggle description in detail view
    $('#description').on('click', function() {
        $('#readme').toggle(300);
    });

    $('#description').on('mouseover', function() {
        $(this).css({color: "#1EAEDB"});
    });

    $('#description').on('mouseout', function() {
        $(this).css({color: "#222"});
    });

    // Toggle commit grouper in commits_by_day view
    $('li[id$="-group"]').on('click', function() {
        var currentNodeId = $(this).attr('id');
        console.log($(this).find('li'));
        $(this).parent().find('li.' + currentNodeId).toggle(300);
    });

    $('li[id$="-group"]').on('mouseover', function() {
        $(this).css({color: "#1EAEDB"});
    });

    $('li[id$="-group"]').on('mouseout', function() {
        $(this).css({color: "#222"});
    });

});
