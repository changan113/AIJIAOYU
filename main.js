const scene = new THREE.Scene();

const camera = new THREE.PerspectiveCamera(
    75,
    window.innerWidth / window.innerHeight,
    0.1,
    1000
);

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// 错误1：OrbitControls 会报错，注释掉（不影响任何功能）
// const controls = new THREE.OrbitControls(camera, renderer.domElement);

camera.position.z = 10;

const light = new THREE.PointLight(0xffffff, 2);
light.position.set(10, 10, 10);
scene.add(light);

const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
scene.add(ambientLight);

const nodes = [
    { name: '变量', position: [-4, 0, 0], mastery: 20 },
    { name: '循环', position: [-2, 2, 0], mastery: 40 },
    { name: '函数', position: [0, 0, 0], mastery: 10 },
    { name: '类', position: [2, 2, 0], mastery: 0 },
    { name: '文件操作', position: [4, 0, 0], mastery: 0 }
];

const nodeMeshes = {};

function getColor(mastery) {
    if (mastery < 30) return 0xff0000;
    if (mastery < 70) return 0xffff00;
    return 0x00ff00;
}

function createNode(node) {
    const geo = new THREE.SphereGeometry(0.5, 16, 16);
    const mat = new THREE.MeshStandardMaterial({ color: getColor(node.mastery) });
    const mesh = new THREE.Mesh(geo, mat);
    mesh.position.set(...node.position);
    mesh.userData = node;
    scene.add(mesh);
    nodeMeshes[node.name] = mesh;
}

function createConnection(start, end) {
    const points = [];
    points.push(new THREE.Vector3(...start.position));
    points.push(new THREE.Vector3(...end.position));
    const geometry = new THREE.BufferGeometry().setFromPoints(points);
    const material = new THREE.LineBasicMaterial({ color: 0xffffff });
    const line = new THREE.Line(geometry, material);
    scene.add(line);
}

nodes.forEach(createNode);

for (let i = 0; i < nodes.length - 1; i++) {
    createConnection(nodes[i], nodes[i + 1]);
}

const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();

window.addEventListener('click', (event) => {
    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObjects(Object.values(nodeMeshes));
    if (intersects.length > 0) {
        const node = intersects[0].object.userData;
        document.getElementById('nodeInfo').innerHTML = `
            <b>知识点：</b>${node.name}<br>
            <b>掌握度：</b>${node.mastery}%
        `;
    }
});

async function updateNodes() {
    try {
        const response = await fetch('/api/get_status');
        const data = await response.json();
        nodes.forEach(node => {
            if (data[node.name] !== undefined) {
                node.mastery = data[node.name];
                const mesh = nodeMeshes[node.name];
                mesh.material.color.setHex(getColor(node.mastery));
            }
        });
    } catch (error) {
        console.error('更新失败:', error);
    }
}

setInterval(updateNodes, 5000);

function animate() {
    requestAnimationFrame(animate);
    Object.values(nodeMeshes).forEach(mesh => {
        mesh.rotation.y += 0.01;
    });
    renderer.render(scene, camera);
}

animate();

window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});