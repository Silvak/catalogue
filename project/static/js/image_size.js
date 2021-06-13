window.onload= inicio;




function inicio(){
      
    for (let i = 0; i <= 602; i++) {


        var img = document.images[i];
        var altoOriginal = img.naturalHeight;
        var anchoOriginal = img.naturalWidth;

        if (altoOriginal > 560 && anchoOriginal < 432){
            var d = 'card'+ i.toString();
            var d = document.getElementById(d);
            d.className = 'card-one ';
            
        } 
        else if (anchoOriginal > 700 &&  altoOriginal < 340 ){
            var d= 'card'+ i.toString();
            var d = document.getElementById(d);
            d.className = 'card-two';
        }

        else if (altoOriginal > 540 && anchoOriginal > 540){
            var d = 'card'+ i.toString();
            var d = document.getElementById(d);
            d.className = 'card-three';
        }
    }
}


