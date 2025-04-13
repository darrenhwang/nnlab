import { useEffect, useRef } from 'react';
import { Box, Typography, Paper, Grid } from '@mui/material';
import { useSelector } from 'react-redux';
import { RootState } from '../store';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';

export default function Visualization() {
  const currentModel = useSelector((state: RootState) => state.model.currentModel);
  const containerRef = useRef<HTMLDivElement>(null);
  const sceneRef = useRef<THREE.Scene | null>(null);
  const cameraRef = useRef<THREE.PerspectiveCamera | null>(null);
  const rendererRef = useRef<THREE.WebGLRenderer | null>(null);
  const controlsRef = useRef<OrbitControls | null>(null);

  useEffect(() => {
    if (!containerRef.current || !currentModel) return;

    // 初始化Three.js场景
    const scene = new THREE.Scene();
    sceneRef.current = scene;
    scene.background = new THREE.Color(0xf0f0f0);

    // 设置相机
    const camera = new THREE.PerspectiveCamera(
      75,
      containerRef.current.clientWidth / containerRef.current.clientHeight,
      0.1,
      1000
    );
    cameraRef.current = camera;
    camera.position.z = 5;

    // 设置渲染器
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    rendererRef.current = renderer;
    renderer.setSize(containerRef.current.clientWidth, containerRef.current.clientHeight);
    containerRef.current.appendChild(renderer.domElement);

    // 添加轨道控制
    const controls = new OrbitControls(camera, renderer.domElement);
    controlsRef.current = controls;
    controls.enableDamping = true;

    // 创建神经网络可视化
    const createNeuralNetwork = () => {
      const layers = currentModel.layers;
      const material = new THREE.MeshPhongMaterial({ color: 0x00ff00 });
      const neuronGeometry = new THREE.SphereGeometry(0.1);
      
      layers.forEach((layer, layerIndex) => {
        const neurons = layer.units;
        const layerGroup = new THREE.Group();
        
        for (let i = 0; i < neurons; i++) {
          const neuron = new THREE.Mesh(neuronGeometry, material);
          const y = (i - neurons / 2) * 0.3;
          neuron.position.set(layerIndex * 2 - layers.length + 1, y, 0);
          layerGroup.add(neuron);

          // 如果不是第一层，添加与前一层的连接
          if (layerIndex > 0) {
            const prevLayer = layers[layerIndex - 1];
            const lineMaterial = new THREE.LineBasicMaterial({ color: 0x0000ff, opacity: 0.2, transparent: true });
            
            for (let j = 0; j < prevLayer.units; j++) {
              const prevY = (j - prevLayer.units / 2) * 0.3;
              const lineGeometry = new THREE.BufferGeometry().setFromPoints([
                new THREE.Vector3(layerIndex * 2 - layers.length - 1, prevY, 0),
                new THREE.Vector3(layerIndex * 2 - layers.length + 1, y, 0),
              ]);
              const line = new THREE.Line(lineGeometry, lineMaterial);
              layerGroup.add(line);
            }
          }
        }
        scene.add(layerGroup);
      });
    };

    // 添加光源
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    scene.add(ambientLight);
    const pointLight = new THREE.PointLight(0xffffff, 1);
    pointLight.position.set(5, 5, 5);
    scene.add(pointLight);

    createNeuralNetwork();

    // 动画循环
    const animate = () => {
      requestAnimationFrame(animate);
      controls.update();
      renderer.render(scene, camera);
    };
    animate();

    // 处理窗口大小变化
    const handleResize = () => {
      if (!containerRef.current) return;
      const width = containerRef.current.clientWidth;
      const height = containerRef.current.clientHeight;
      
      if (cameraRef.current) {
        cameraRef.current.aspect = width / height;
        cameraRef.current.updateProjectionMatrix();
      }
      
      if (rendererRef.current) {
        rendererRef.current.setSize(width, height);
      }
    };
    window.addEventListener('resize', handleResize);

    // 清理函数
    return () => {
      window.removeEventListener('resize', handleResize);
      if (containerRef.current && rendererRef.current) {
        containerRef.current.removeChild(rendererRef.current.domElement);
      }
      scene.clear();
    };
  }, [currentModel]);

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        网络可视化
      </Typography>

      <Grid container spacing={2}>
        <Grid item xs={12}>
          <Paper sx={{ p: 2, mb: 2 }}>
            <Typography variant="h6" gutterBottom>
              当前模型: {currentModel?.name || '未选择模型'}
            </Typography>
          </Paper>
        </Grid>

        <Grid item xs={12}>
          <Paper
            ref={containerRef}
            sx={{
              width: '100%',
              height: '600px',
              overflow: 'hidden',
            }}
          />
        </Grid>
      </Grid>
    </Box>
  );
} 