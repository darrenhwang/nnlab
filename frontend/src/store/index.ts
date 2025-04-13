import { configureStore } from '@reduxjs/toolkit'
import modelReducer from './slices/modelSlice'
import trainingReducer from './slices/trainingSlice'
import authReducer from './slices/authSlice'

export const store = configureStore({
  reducer: {
    model: modelReducer,
    training: trainingReducer,
    auth: authReducer,
  },
})

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch 