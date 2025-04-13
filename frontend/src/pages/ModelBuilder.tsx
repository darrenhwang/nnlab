import { useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  Button,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Grid,
} from '@mui/material';
import { useDispatch } from 'react-redux';
import { setCurrentModel } from '../store/slices/modelSlice';

interface Layer {
  id: string;
  type: string;
  units: number;
  activation: string;
}

export default function ModelBuilder() {
  const dispatch = useDispatch();
  const [layers, setLayers] = useState<Layer[]>([]);
  const [modelName, setModelName] = useState('');

  const activationFunctions = ['relu', 'sigmoid', 'tanh', 'softmax'];
  const layerTypes = ['dense', 'conv2d', 'maxpool2d'];

  const addLayer = () => {
    const newLayer: Layer = {
      id: `layer-${layers.length}`,
      type: 'dense',
      units: 64,
      activation: 'relu',
    };
    setLayers([...layers, newLayer]);
  };

  const updateLayer = (index: number, field: keyof Layer, value: string | number) => {
    const updatedLayers = layers.map((layer, i) => {
      if (i === index) {
        return { ...layer, [field]: value };
      }
      return layer;
    });
    setLayers(updatedLayers);
  };

  const removeLayer = (index: number) => {
    setLayers(layers.filter((_, i) => i !== index));
  };

  const handleSave = () => {
    const model = {
      id: Date.now().toString(),
      name: modelName,
      layers,
      status: 'created',
    };
    dispatch(setCurrentModel(model));
  };

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        模型构建器
      </Typography>

      <Paper sx={{ p: 2, mb: 2 }}>
        <TextField
          fullWidth
          label="模型名称"
          value={modelName}
          onChange={(e) => setModelName(e.target.value)}
          sx={{ mb: 2 }}
        />

        {layers.map((layer, index) => (
          <Box key={layer.id} sx={{ mb: 2, p: 2, border: '1px solid #eee' }}>
            <Grid container spacing={2} alignItems="center">
              <Grid item xs={3}>
                <FormControl fullWidth>
                  <InputLabel>层类型</InputLabel>
                  <Select
                    value={layer.type}
                    label="层类型"
                    onChange={(e) => updateLayer(index, 'type', e.target.value)}
                  >
                    {layerTypes.map((type) => (
                      <MenuItem key={type} value={type}>
                        {type}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={3}>
                <TextField
                  fullWidth
                  label="神经元数量"
                  type="number"
                  value={layer.units}
                  onChange={(e) => updateLayer(index, 'units', parseInt(e.target.value))}
                />
              </Grid>
              <Grid item xs={3}>
                <FormControl fullWidth>
                  <InputLabel>激活函数</InputLabel>
                  <Select
                    value={layer.activation}
                    label="激活函数"
                    onChange={(e) => updateLayer(index, 'activation', e.target.value)}
                  >
                    {activationFunctions.map((func) => (
                      <MenuItem key={func} value={func}>
                        {func}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={3}>
                <Button
                  variant="outlined"
                  color="error"
                  onClick={() => removeLayer(index)}
                >
                  删除
                </Button>
              </Grid>
            </Grid>
          </Box>
        ))}

        <Button variant="contained" onClick={addLayer} sx={{ mr: 1 }}>
          添加层
        </Button>
        <Button
          variant="contained"
          color="primary"
          onClick={handleSave}
          disabled={!modelName || layers.length === 0}
        >
          保存模型
        </Button>
      </Paper>
    </Box>
  );
} 