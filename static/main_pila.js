/////////////////////////////////////////////////////////////////////////////////////////////////////////
// DataTable yfdt
/////////////////////////////////////////////////////////////////////////////////////////////////////////
yangtb = ''
var yfdt = function(json, ydivmon, ytablemon, yy=730, yorder=false) {
    console.log('Start yfdt !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!');
    if (json.columns.length > 0) {
        var tableHeaders = "";

        $.each(json.columns, function(i, val){
            tableHeaders += "<th>" + val + "</th>";
        });
        $('#' + ydivmon).empty();
        $('#' + ydivmon).append('<table id="' + ytablemon + '" class="table table-bordered display dtytable" cellspacing="0" width="100%"><thead><tr class="success">' + tableHeaders + '</tr></thead></table>');

        yangtb = $('#' + ytablemon).removeAttr('width').DataTable({
            "destroy": true,
            "data": json.data,
//            "dom": 'Bfrtip',
//            "buttons": [
//                'copy', 'csv', 'excel', 'pdf'
//            ],
            "scrollY": yy,
            "paging" : false,
            "AutoWidth": false,
            "FixedHeader": true,
            "ordering": yorder,
            "columnDefs": [
                { "targets": [0],   //30
                   "width": "9%"
                }
            ]
        });

    }else {
        console.log("Yang Error json.length == 0")
    }
}



var yDatatables = function(yurl, ydiv, ytable, yy=400, yorder=false) {
    console.log("START yDatatables yfdt : " + yurl + " , " + ydiv + " , " + ytable)
    $.ajax({
        "url": '/' + yurl,  //"url": '/Ajob',
        "dataType": "json",
        "success": function(json) {
            yfdt(json, ydiv, ytable, yy, yorder);
        }
    });
}
var yDatatablesMan = function(yurl, ydiv, ytable, apara1, yy=650, yorder=false) {
    console.log("START yDatatablesMan yfdt : " + yurl + " , " + ydiv  + " , " + ytable + " , " + apara1)
    $.ajax({
        "url": '/' + yurl,  //"url": '/Ajob',
        "dataType": "json",
        "data": {
            'ys1' : apara1
        },
        "success": function(json) {
            yfdt(json, ydiv, ytable, yy, yorder);
        }
    });
}




ydtvocold = ''
//////////////  Dom /////////////////////////////////////////////////////////////////////////////////////////////
//////////////  Dom /////////////////////////////////////////////////////////////////////////////////////////////
$(document).ready(function() {
    $("#tabs").tabs({
        activate: function( event, ui ){
            var selectedTab = $("#tabs").tabs('option', 'active'); // 선택된 tab의 index value
            if(selectedTab == 0){
                $("#tabs").tabs({ active: 0 })
                yDatatables('APRES', "ydiv0", "ytable0", 700);
            } else if(selectedTab == 1){
                $("#tabs").tabs({ active: 1 })
                yDatatables('ACUST', "ydiv1", "ytable1", 700);
            } else if(selectedTab == 2){
                $("#tabs").tabs({ active: 2 })
                yDatatables('APEOP', "ydiv2", "ytable2", 700);
            }  else if(selectedTab == 3){
                $("#tabs").tabs({ active: 3 })
                yDatatables('AREGI', "ydiv3", "ytable3", 700);
            }  else if(selectedTab == 4){
                $("#tabs").tabs({ active: 4 })
                yDatatables('AWORK', "ydiv4", "ytable4", 700);
            }  else if(selectedTab == 5){
                $("#tabs").tabs({ active: 5 })
                yDatatables('AGOOD', "ydiv5", "ytable5", 700);
            }  else if(selectedTab == 6){
                $("#tabs").tabs({ active: 6 })
                yDatatables('AMORE', "ydiv6", "ytable6", 700);
            }  else if(selectedTab == 7){
                $("#tabs").tabs({ active: 7 })
                yDatatables('APAY', "ydiv7", "ytable7", 700, true);
            }  else if(selectedTab == 8){
                $("#tabs").tabs({ active: 8 })
                yDatatables('ASCHA', "ydiv81", "ytable81", 200);
                yDatatables('ASCHB', "ydiv82", "ytable82", 200);
                yDatatables('ASCHC', "ydiv83", "ytable83", 200);
            }
        }
    });

    // datepicker ////////////////////////////////////////////////////////////
    $( "#datepickersch82" ).datepicker({
        dateFormat: 'yy-mm-dd',
        showOtherMonths: true,
        selectOtherMonths: true,
        showButtonPanel: true,
        //minDate: -31,
        //maxDate: "+0D"
    });
    
//////////////  최초시작 /////////////////////////////////////////////////////////////////////////////////////////////
    yDatatables('APRES', "ydiv0", "ytable0", 700);

///////////////////////////////////////////////////////////////////////////////////////////////////////
// 1분마다
///////////////////////////////////////////////////////////////////////////////////////////////////////


//    window.setInterval(function(){
//        console.log('Sched Start1 !!!');
//        $.ajax({
//            url: '/AServer',   //'static/testdata/arrays_short2.txt',  //'/AjaxTable1_4',
//            dataType: "json", //ydtstr4
//            success: function(json) {
//                console.log(json);
//    //            var yvocdtnew = json;
//    //            $("#btn_TopR1").val('UPDATE시각:' + yvocdtnew);
//    //            ydtvocold = yvocdtnew;
//            }
//        });
//        yDatatablestop('AjaxTable0', "ydiv0", "ytable0", 150);
//        yDatatables('AjaxTable1', "ydiv1", "ytable1", 300);
//        yDatatables('AjaxTable12', "ydiv12", "ytable12", 200);
//    }, 120*1000);  //interval 120초


//////////////  Event /////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////
// Event
/////////////////////////////////////////////////////////////////////////////////////////////////////////
    $('ytable').on( 'click', 'tbody tr', function () {
        if ( $(this).hasClass('selected') ) {
            $(this).removeClass('selected');
        }
        else {
            $(this).addClass('selected');
        }
    });

    $('#ydiv1').on('dblclick', 'tbody td', function() {
        var td_val = $(this).text();
        var td_icol = $(this).index();
        var tbid = $(this).closest('table').attr('id');

        var td_first = $(this).siblings("td:first").text();

        console.log('dbclicked :' + td_val + ' , ' + td_icol.toString() + ' , ' + tbid  + ' , ' + td_first);
        if (td_icol == 0){
            if (td_val.length > 2) {
                $('#yModal').modal('show');
                setTimeout(function(){
                    yDatatablesMan('AjaxMan', 'ydivmodal', 'ytablemodal', td_val, 450);
                    // $("#ycomma").val(comma);
                }, 1000);
            }
        }
    });



    $('#btn_query').click(function(){
        var ymanqry = $( "#qry_filter" ).val();
        console.log("Clicked btn_query : " + ymanqry)
        if (ymanqry.length > 2) {
            yDatatablesMan('AjaxMan', 'ydiv9', 'ytable9', ymanqry, 650);
        }

    });



} );





