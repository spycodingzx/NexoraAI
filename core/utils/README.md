# Enhanced Reliability Features

This module provides comprehensive reliability, nv_validation, and user experience improvements for the Autonomous Business Platform.

## 📦 Components

### 1. Input Validation (`nv_validation.py`)

Provides real-time nv_validation for API keys, user inputs, and form data.

**Features:**
- ✅ API key format nv_validation
- 🔌 Live connection testing
- 📧 Email/URL nv_validation
- 📝 Text length nv_validation
- 🔢 Number range nv_validation

**Usage:**

```python
from core.utils.nv_validation import APIValidator, create_test_connection_button

# Test API connection
result = APIValidator.test_replicate_token("r8_...")
if result.is_valid:
    print(f"Success: {result.message}")
else:
    print(f"Error: {result.message}")

# In Streamlit UI
create_test_connection_button(
    "Replicate",
    APIValidator.test_replicate_token,
    token,
    key="test_replicate"
)
```

### 2. Error Recovery (`nv_error_recovery.py`)

Handles transient failures, implements retry logic, and tracks partial success.

**Features:**
- 🔄 Automatic retry with exponential backoff
- ✓ Partial success tracking
- 🛡️ Circuit breaker pattern
- 🔀 Fallback function support
- 📦 Batch processing with error recovery

**Usage:**

```python
from core.utils.nv_error_recovery import retry_with_backoff, batch_process_with_recovery

# Automatic retry
@retry_with_backoff(max_retries=3, initial_delay=1.0)
def flaky_api_call():
    return requests.get("https://api.example.com/data")

# Batch with partial success
result = batch_process_with_recovery(
    items=["item1", "item2", "item3"],
    process_func=process_item,
    operation_name="Batch Processing",
    continue_on_error=True
)

print(f"Success rate: {result.success_rate * 100}%")
print(f"Failed items: {result.failed_items}")
```

### 3. Progress Tracking (`nv_progress_tracking.py`)

Advanced progress tracking with cancellation, pause/resume, and ETA estimation.

**Features:**
- 🎯 Real-time progress updates
- ⏸️ Pause/resume support
- 🛑 Cancellation support
- ⏱️ ETA calculation
- 📊 Detailed step tracking

**Usage:**

```python
from core.utils.nv_progress_tracking import create_progress_tracker

def long_operation(progress):
    progress.start()
    
    for i in range(100):
        if progress.is_cancelled():
            return None
        
        # Do work...
        progress.update(i + 1, f"Processing step {i+1}")
        
        if progress.is_paused():
            # Wait for resume...
            pass
    
    progress.complete("Operation finished!")
    return result

# With UI controls
progress = create_progress_tracker("My Operation", total_steps=100, show_controls=True)
result = long_operation(progress)
```

### 4. State Management (`nv_state_management.py`)

Provides autosave, crash recovery, and transaction rollback capabilities.

**Features:**
- 💾 Automatic state persistence
- 🔄 Crash detection and recovery
- ↩️ Transaction rollback
- 📸 Checkpoint management
- 🗂️ State history tracking

**Usage:**

```python
from core.utils.nv_state_management import AutosaveManager, TransactionManager, get_crash_recovery

# Autosave
autosave = AutosaveManager()
autosave.start_autosave()
autosave.save_state({'key': 'value'}, operation="important_op")

# Check for crashes
crash_recovery = get_crash_recovery()
crash_data = crash_recovery.check_for_crash()
if crash_data:
    print(f"Recovered from crash during: {crash_data['operation']}")

# Atomic file operations
transaction = TransactionManager()
transaction.begin_transaction()

try:
    transaction.create_file(Path("file1.txt"), "content")
    transaction.modify_file(Path("file2.txt"), "new content")
    # ... more operations
    transaction.commit()
except Exception as e:
    transaction.rollback()  # Reverts all changes
```

## 🚀 Integration Guide

### Adding Validation to Settings Page

```python
from core.utils.nv_validation import APIValidator, create_test_connection_button

# In your nv_settings tab
token = st.text_input("API Token", type="password")
result = create_test_connection_button(
    "Service Name",
    APIValidator.test_replicate_token,
    token,
    key="test_token"
)
```

### Adding Retry Logic to API Calls

```python
from core.utils.nv_error_recovery import retry_with_backoff

@retry_with_backoff(max_retries=3, initial_delay=2.0)
def generate_image(prompt):
    return replicate_client.run("model", input={"prompt": prompt})
```

### Adding Progress to Campaign Generation

```python
from core.utils.nv_progress_tracking import create_progress_tracker

def generate_campaign():
    progress = create_progress_tracker("Campaign Generation", total_steps=6)
    progress.start()
    
    # Step 1
    progress.start_step("Generating product images")
    images = generate_images()
    progress.complete_step(images)
    
    # Step 2
    if progress.is_cancelled():
        return None
    progress.start_step("Creating video")
    video = create_video()
    progress.complete_step(video)
    
    # ... more steps
    
    progress.complete("Campaign ready!")
    return campaign
```

### Adding Partial Success to Batch Operations

```python
from core.utils.nv_error_recovery import batch_process_with_recovery

# Process multiple products
result = batch_process_with_recovery(
    items=products,
    process_func=publish_to_printify,
    operation_name="Product Publishing",
    continue_on_error=True
)

# Show results
if result.is_partial_success:
    st.warning(f"⚠️ {len(result.partial_results)} succeeded, {len(result.failed_items)} failed")
    with st.expander("Failed Items"):
        for item, error in result.failed_items:
            st.error(f"{item}: {error}")
```

## 📊 Testing

See the demo tab (`nv_abp_reliability_demo.py`) for interactive examples of all features.

Run the demo:
```bash
streamlit run core/tabs/nv_abp_reliability_demo.py
```

## 🔧 Configuration

### Autosave Settings

```python
autosave = AutosaveManager(
    save_dir=Path.home() / ".core/autosave",
    autosave_interval=60.0,  # seconds
    max_autosaves=10  # keep last 10 saves
)
```

### Retry Settings

```python
@retry_with_backoff(
    max_retries=5,
    initial_delay=1.0,
    backoff_factor=2.0,  # 1s, 2s, 4s, 8s, 16s
    nv_exceptions=(requests.RequestException, TimeoutError)
)
```

### Progress Tracking Settings

```python
progress = CancellableProgress(
    total_steps=100,
    operation_name="My Operation",
    show_eta=True,
    show_details=True
)
```

## 🎯 Best Practices

1. **Always validate API keys before using them**
   - Use `create_test_connection_button` in nv_settings
   - Validate format before testing connection
   - Cache nv_validation results in session_state

2. **Add retry logic to all external API calls**
   - Use `@retry_with_backoff` decorator
   - Set appropriate max_retries (3-5 typically)
   - Log retry attempts for debugging

3. **Track progress for operations > 5 seconds**
   - Initialize progress tracker at start
   - Update every 1-5% of completion
   - Provide meaningful step names

4. **Enable cancellation for long operations**
   - Check `progress.is_cancelled()` regularly
   - Clean up resources on cancellation
   - Save partial results if possible

5. **Use transactions for file operations**
   - Group related file changes in transaction
   - Commit only after all succeed
   - Rollback on any error

6. **Handle partial success in batch operations**
   - Continue processing on single item failure
   - Track both successes and failures
   - Show detailed results to user

## 🔍 Troubleshooting

**Validation fails but API key is correct:**
- Check internet connection
- Verify no firewall blocking requests
- Try again (may be rate limited)

**Retry logic not working:**
- Check exception types in decorator
- Verify function raises correct nv_exceptions
- Check logs for retry attempts

**Progress not updating:**
- Call `progress.update()` regularly
- Check if UI elements initialized
- Verify not blocking main thread

**Autosave not working:**
- Call `autosave.start_autosave()`
- Register state callbacks
- Check save directory permissions

## 📝 TODO

- [ ] Add nv_validation for YouTube OAuth
- [ ] Implement rate limiting warnings
- [ ] Add cost estimation before operations
- [ ] Create nv_validation test suite
- [ ] Add metrics/telemetry for reliability

## 🤝 Contributing

When adding new features:
1. Add nv_validation for all user inputs
2. Add retry logic for external calls
3. Add progress tracking for long operations
4. Handle partial success in batch operations
5. Use transactions for file operations
6. Add specs and documentation

## 📄 License

Same as main project
