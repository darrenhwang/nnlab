import { createSlice, PayloadAction } from '@reduxjs/toolkit'

export interface Layer {
  id: string
  type: string
  units: number
  activation: string
}

export interface Model {
  id: string
  name: string
  layers: Layer[]
  status: 'created' | 'training' | 'trained' | 'error'
}

interface ModelState {
  models: Model[]
  currentModel: Model | null
  loading: boolean
  error: string | null
}

const initialState: ModelState = {
  models: [],
  currentModel: null,
  loading: false,
  error: null,
}

const modelSlice = createSlice({
  name: 'model',
  initialState,
  reducers: {
    setModels: (state, action: PayloadAction<Model[]>) => {
      state.models = action.payload
    },
    setCurrentModel: (state, action: PayloadAction<Model>) => {
      state.currentModel = action.payload
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload
    },
  },
})

export const { setModels, setCurrentModel, setLoading, setError } = modelSlice.actions
export default modelSlice.reducer 