$(document).ready(()=>{

	function ask(){
		$.ajax({
			url: $("#url").val(),
			success: (data)=> {
				try {
					console.log(data);
					let x = JSON.parse(data),
						today = new Date(),
						date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate(),
						time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds(),
						dateTime = date+' '+ time;
	
					x = dateTime + "<br>" + JSON.stringify(x);
					$(".output").html(x);
					$(".output").css('color', 'black');
				} catch (e) {
					$(".output").html("ERROR!<br>" + e + "<hr>" + data);
				}
				
			},
			error: (data)=>{
				$(".output").html(data.responseText);
				$(".output").css('color', 'red');
			}
		})
	}

	$("#run").on('click', ask);
	$("#url").on('keypress', (event)=>{
		if (event.keyCode === 13) {
			ask();
		}
	});

	$("#recent li").on('click', (event)=>{
		$("#url").val(event.target.innerHTML);
	});


});
