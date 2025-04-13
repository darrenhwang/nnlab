import { Box, CssBaseline, ThemeProvider } from '@mui/material';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Provider } from 'react-redux';
import { store } from './store';
import theme from './theme';
import Layout from './components/common/Layout';
import Home from './pages/Home';
import ModelBuilder from './pages/ModelBuilder';
import Training from './pages/Training';
import Visualization from './pages/Visualization';

function App() {
  return (
    <Provider store={store}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Box sx={{ display: 'flex' }}>
          <Router>
            <Layout>
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/model-builder" element={<ModelBuilder />} />
                <Route path="/training" element={<Training />} />
                <Route path="/visualization" element={<Visualization />} />
              </Routes>
            </Layout>
          </Router>
        </Box>
      </ThemeProvider>
    </Provider>
  );
}

export default App; 