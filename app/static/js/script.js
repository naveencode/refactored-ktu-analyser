// window.alert("Helo")


function load_page(exam_id, college_id = null, dept_id = null) {
    const request = new XMLHttpRequest();
    if(! (college_id || dept_id))
        request.open('GET', `/api/exams/${exam_id}`);
    else if(college_id)
        request.open('GET', `/api/exam/${exam_id}/colleges/${college_id}`);
    else if(dept_id)
        request.open('GET', `/api/exam/${exam_id}/colleges/${college_id}/departments/${dept_id}`);
    
    request.onload = () => {
        const data = JSON.parse(request.responseText);
        createTable(data);
    }
    request.send()

        
}

function createTable(data) {
    data['college_pass_percentage'].sort(function (a,b) {
        return a[1] > b[1] ? -1 : 1;
    });
    var body = document.getElementsByTagName('body')[0];
    var tbl = document.createElement('table');
    // tbl.createCaption();
    // tbl.innerHTML = `<b> ${data['exam_name']} </b>`;
    tbl.style.width = '100%';
    tbl.setAttribute('border', '1');
    var tbdy = document.createElement('tbody');

    var tr = document.createElement('tr');
    var th = document.createElement('th');
    th.appendChild(document.createTextNode('Rank'));
    tr.appendChild(th)

    th = document.createElement('th');
    th.appendChild(document.createTextNode('College Name'));
    tr.appendChild(th)

    th = document.createElement('th');
    th.appendChild(document.createTextNode('Pass Percentage'));
    tr.appendChild(th)
    tbdy.appendChild(tr);
    
    for(var i = 0; i < data['college_pass_percentage'].length; i++)
    {
        var tr = document.createElement('tr');
        for(var j = 0; j < 3; j++)
        {
            var td = document.createElement('td');
            if(j == 0) {
                td.appendChild(document.createTextNode(`${i+1}`));
                td.setAttribute('align', 'center');
            }
            else if(j == 1) {
                td.appendChild(document.createTextNode(`${data['college_pass_percentage'][i][j-1]}`));
            }
            else {
                td.appendChild(document.createTextNode(`${data['college_pass_percentage'][i][j-1].toFixed(2)}`));
                td.setAttribute('align', 'center');
            }
                
            tr.appendChild(td)
        }
        tbdy.appendChild(tr);
    }
    tbl.appendChild(tbdy);
    body.appendChild(tbl);


}

document.getElementById("exam-btn").addEventListener("click", function(){
    var exam_id = document.getElementById('my-select').value
    load_page(exam_id);
});
