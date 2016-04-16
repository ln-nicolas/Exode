function random(a,b){
  return Math.floor((Math.random() * b) + a);
}

function sup(a,b){ return((a>b) ? a : b) }


function H(i){
    r= random(Math.cos(i*0.314+3.14)*4,Math.cos(i*0.314+3.14)*4+0.0);
    return r;
}

var renderer = new THREE.WebGLRenderer({alpha:true})
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);
var camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 1, 100);
camera.position.set(0, 15, 70);

var scene = new THREE.Scene();


var cubes = {}

function initCubes() {
    for (var i = -20; i <= 20; i++) {
        cubes[i] = {}
        for (var j = 10; j > -20; j--) {

            var geometry = new THREE.CubeGeometry(2.8, H(i), 2.8);

            var cubeMaterials = [];
            for (var f = 0; f < 6; f++)
                cubeMaterials[f] = new THREE.MeshBasicMaterial({
                    color: 0x211a47,
                    transparent: true,
                    opacity: 0.8,
                    side: THREE.DoubleSide
                });

            var cubeMaterial = new THREE.MeshFaceMaterial(cubeMaterials);
            var cube = new THREE.Mesh(geometry, cubeMaterial);
            cube.position.set(i * 3, geometry.parameters.height / 2, j * 3 - 10);

            cubes[i][j] = cube;
            scene.add(cube);
        }
    }
}
initCubes();


function cube(i,j){
    return cubes[i][j]
}


// global for camera
var t=1, t_max= 1.5;
function goTo(stop){ t_max= stop; }

var render = function () {
    requestAnimationFrame(render);
    if(Math.abs(t-t_max)>0.01){
        t+= (Math.abs(t_max-t)/(t_max-t))*Math.abs(t_max-t)*0.1;
        camera.position.z = 70-t*t*t;
        camera.position.y = 15/t;
    }
    renderer.render(scene, camera);
};
render();

var winResize   = new THREEx.WindowResize(renderer, camera);