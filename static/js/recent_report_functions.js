function recent_report_one() {
    let case_number = document.getElementById('report_one_number');
    let id_number = case_number.innerHTML;

    let county = document.getElementById('repo-one').innerHTML;
    let new_county = county.split(',')[1].trim()

    fetch('/report_one_pass', {
        method: 'POST',
        body: JSON.stringify({ id: id_number, county: new_county }),
        headers: {
          'Content-Type': 'application/json'
        }
      })
}




function recent_report_two() {
    let case_number = document.getElementById('report_two_number');
    let id_number = case_number.innerHTML;

    let county = document.getElementById('repo-two').innerHTML;
    let new_county = county.split(',')[1].trim()

    fetch('/report_two_pass', {
        method: 'POST',
        body: JSON.stringify({ id: id_number, county: new_county }),
        headers: {
          'Content-Type': 'application/json'
        }
      })
}




function recent_report_three() {
    let case_number = document.getElementById('report_three_number');
    let id_number = case_number.innerHTML;

    let county = document.getElementById('repo-three').innerHTML;
    let new_county = county.split(',')[1].trim()

    fetch('/report_three_pass', {
        method: 'POST',
        body: JSON.stringify({ id: id_number, county: new_county }),
        headers: {
          'Content-Type': 'application/json'
        }
      })
}
