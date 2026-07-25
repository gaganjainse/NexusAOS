use std::sync::Mutex;

use tauri::State;

use crate::model::DashboardSnapshot;
use crate::state::NexusState;

#[tauri::command]
pub fn snapshot(state: State<'_, Mutex<NexusState>>) -> DashboardSnapshot {
    state.lock().expect("state lock poisoned").snapshot()
}

#[tauri::command]
pub fn tick_state(state: State<'_, Mutex<NexusState>>) -> DashboardSnapshot {
    state.lock().expect("state lock poisoned").tick()
}

#[tauri::command]
pub fn mutate_genome(state: State<'_, Mutex<NexusState>>) -> DashboardSnapshot {
    state.lock().expect("state lock poisoned").mutate()
}

#[tauri::command]
pub fn reset_state(state: State<'_, Mutex<NexusState>>) -> DashboardSnapshot {
    state.lock().expect("state lock poisoned").reset()
}
