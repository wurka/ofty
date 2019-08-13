var fff = 444;
var b_server = 'localhost:9000';
var f_server = 'localhost:8080';




function hey() {
  //alert('HEEEY!');
  //let x = axios.get('http://localhost:8000//units/get-group-parameters?groupid=70');
  console.log('x');
}

function myajax(url,mydata) {
  $.ajax({
    url: b_server+url,
    data: mydata,
    method: "GET",
    success: (data)=> {
      try {
        console.log(data);
        let x = JSON.parse(data);
        return(JSON.stringify(x));
      } catch (e) {
        console.log("ERROR!: \n" + e + " \n" + data);
      }

    },
    error: (data)=>{
      console.log("Ajax ERROR!");
      console.log(data);
    }
  })
}
function b_ax(ax) {
  return (ax.create({
    baseURL: 'http://localhost:9000/'
  }))
}

/*document.ready(){
  axios({
    method:'post',
    url:'http://localhost:8000/units/add-new-unit',
    data: {'csrfmiddlewaretoken':data1.data},
    headers:{'X-CSRFToken': data1.data}
  })
}*/
