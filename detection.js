let diseasePic = document.getElementById('disease-pic');
let input = document.getElementById('input_file');


input.onchange = (e) => {
       if (input.files[0])
              diseasePic.src = URL.createObjectURL(input.files[0]);
};