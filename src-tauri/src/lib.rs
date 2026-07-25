mod commands;
mod model;
mod state;

use std::sync::Mutex;

use state::NexusState;

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .manage(Mutex::new(NexusState::default()))
        .invoke_handler(tauri::generate_handler![
            commands::snapshot,
            commands::tick_state,
            commands::mutate_genome,
            commands::reset_state,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
