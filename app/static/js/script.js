// // window.alert("Helo")
// document.getElementById("exam-btn").addEventListener("click", function(){
//     var exam_id = document.getElementById('my-select').value
//     load_page(exam_id);
// });


// function load_page(exam_id, college_id = null, dept_id = null) {
//     const request = new XMLHttpRequest();
//     if(! (college_id || dept_id))
//         request.open('GET', `/api/exams/${exam_id}`);
//     else if(college_id)
//         request.open('GET', `/api/exam/${exam_id}/colleges/${college_id}`);
//     else if(dept_id)
//         request.open('GET', `/api/exam/${exam_id}/colleges/${college_id}/departments/${dept_id}`);
    
//     request.onload = () => {
//         const data = JSON.parse(request.responseText);
//         createTable(data);
//     }
//     request.send()

        
// }

// function createTable(data) {
//     data['college_pass_percentage'].sort(function (a,b) {
//         return a[1] > b[1] ? -1 : 1;
//     });
//     var body = document.getElementsByTagName('body')[0];
//     var tbl = document.createElement('table');
//     // tbl.createCaption();
//     // tbl.innerHTML = `<b> ${data['exam_name']} </b>`;
//     tbl.style.width = '100%';
//     tbl.setAttribute('border', '1');
//     var tbdy = document.createElement('tbody');

//     var tr = document.createElement('tr');
//     var th = document.createElement('th');
//     th.appendChild(document.createTextNode('Rank'));
//     tr.appendChild(th)

//     th = document.createElement('th');
//     th.appendChild(document.createTextNode('College Name'));
//     tr.appendChild(th)

//     th = document.createElement('th');
//     th.appendChild(document.createTextNode('Pass Percentage'));
//     tr.appendChild(th)
//     tbdy.appendChild(tr);
    
//     for(var i = 0; i < data['college_pass_percentage'].length; i++)
//     {
//         var tr = document.createElement('tr');
//         for(var j = 0; j < 3; j++)
//         {
//             var td = document.createElement('td');
//             if(j == 0) {
//                 td.appendChild(document.createTextNode(`${i+1}`));
//                 td.setAttribute('align', 'center');
//             }
//             else if(j == 1) {
//                 td.appendChild(document.createTextNode(`${data['college_pass_percentage'][i][j-1]}`));
//             }
//             else {
//                 td.appendChild(document.createTextNode(`${data['college_pass_percentage'][i][j-1].toFixed(2)}`));
//                 td.setAttribute('align', 'center');
//             }
                
//             tr.appendChild(td)
//         }
//         tbdy.appendChild(tr);
//     }
//     tbl.appendChild(tbdy);
//     body.appendChild(tbl);
// }

function sortTable() {
    var table, rows, switching, i, x, y, shouldSwitch;
    table = document.getElementById("my-table");
    switching = true;
    order = table.getAttribute('data-order');
    /* Make a loop that will continue until
    no switching has been done: */
    while (switching) {
      // Start by saying: no switching is done:
      switching = false;
      rows = table.getElementsByTagName("TR");
      /* Loop through all table rows (except the
      first, which contains table headers): */
      for (i = 1; i < (rows.length - 1); i++) {
        // Start by saying there should be no switching:
        shouldSwitch = false;
        /* Get the two elements you want to compare,
        one from current row and one from the next: */
        x = rows[i].getElementsByTagName("TD")[2];
        y = rows[i + 1].getElementsByTagName("TD")[2];
        // Check if the two rows should switch place:
        if (order == "dec") {
            if (parseFloat(x.innerHTML) < parseFloat(y.innerHTML)) {
                // If so, mark as a switch and break the loop:
                shouldSwitch = true;
                break;
              }
        }
        else {
            if (parseFloat(x.innerHTML) > parseFloat(y.innerHTML)) {
                // If so, mark as a switch and break the loop:
                shouldSwitch = true;
                break;
              }
        }
        
      }
      if (shouldSwitch) {
        /* If a switch has been marked, make the switch
        and mark that a switch has been done: */
        rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
        switching = true;
      }
    }
    if (order == "dec") table.setAttribute('data-order', 'asc');
    else  table.setAttribute('data-order', 'dec');
    setRank(table);
  }

  function setRank(table) {
      order = table.getAttribute('data-order');
      rows = table.getElementsByTagName("TR");
      rows[0].getElementsByTagName("TH")[0].innerHTML = "Rank"
      if (order == "asc")
      for (i = 1; i < (rows.length); i++) {
          rows[i].getElementsByTagName("TD")[0].innerHTML = i;
      }
      else {
        for (i = 1; i < (rows.length); i++) {
            rows[i].getElementsByTagName("TD")[0].innerHTML = rows.length-i;
        }
      }
  }