
我们支持以下字段类型：

- `string`：文本输入框。

  ```lms_code_snippet
    variants:
      TypeScript:
        language: typescript
        code: |
          // ... other fields ...
          .field(
            "stringField", // The key of the field.
            "string", // Type of the field.
            {
              displayName: "A string field",
              subtitle: "Subtitle", // Optional subtitle for the field. (Show below the field)
              hint: "Hint", // Optional hint for the field. (Show on hover)
              isParagraph: false, // Whether to show a large text input area for this field.
              isProtected: false, // Whether the value should be obscured in the UI (e.g., for passwords).
              placeholder: "Placeholder text", // Optional placeholder text for the field.
            },
            "default value", // Default Value
          )
          // ... other fields ...
  ```

- `numeric`：数字输入框，可选校验和滑块界面。

  ```lms_code_snippet
    variants:
      TypeScript:
        language: typescript
        code: |
          // ... other fields ...
          .field(
            "numberField", // The key of the field.
            "numeric", // Type of the field.
            {
              displayName: "A number field",
              subtitle: "Subtitle for", // Optional subtitle for the field. (Show below the field)
              hint: "Hint for number field", // Optional hint for the field. (Show on hover)
              int: false, // Whether the field should accept only integer values.
              min: 0, // Minimum value for the field.
              max: 100, // Maximum value for the field.
              slider: {
                // If present, configurations for the slider UI
                min: 0, // Minimum value for the slider.
                max: 100, // Maximum value for the slider.
                step: 1, // Step value for the slider.
              },
            },
            42, // Default Value
          )
          // ... other fields ...
  ```

- `boolean`：复选框或开关输入框。

  ```lms_code_snippet
    variants:
      TypeScript:
        language: typescript
        code: |
          // ... other fields ...
          .field(
            "booleanField", // The key of the field.
            "boolean", // Type of the field.
            {
              displayName: "A boolean field",
              subtitle: "Subtitle", // Optional subtitle for the field. (Show below the field)
              hint: "Hint", // Optional hint for the field. (Show on hover)
            },
            true, // Default Value
          )
          // ... other fields ...
  ```

- `stringArray`：带可配置约束条件的字符串数组。

  ```lms_code_snippet
    variants:
      TypeScript:
        language: typescript
        code: |
          // ... other fields ...
          .field(
            "stringArrayField",
            "stringArray",
            {
              displayName: "A string array field",
              subtitle: "Subtitle", // Optional subtitle for the field. (Show below the field)
              hint: "Hint", // Optional hint for the field. (Show on hover)
              allowEmptyStrings: true, // Whether to allow empty strings in the array.
              maxNumItems: 5, // Maximum number of items in the array.
            },
            ["default", "values"], // Default Value
          )
          // ... other fields ...
  ```

- `select`：带预定义选项的下拉选择框。

  ```lms_code_snippet
    variants:
      TypeScript:
        language: typescript
        code: |
          // ... other fields ...
          .field(
            "selectField",
            "select",
            {
              displayName: "A select field",
              options: [
                { value: "option1", displayName: "Option 1" },
                { value: "option2", displayName: "Option 2" },
                { value: "option3", displayName: "Option 3" },
              ],
              subtitle: "Subtitle", // Optional subtitle for the field. (Show below the field)
              hint: "Hint", // Optional hint for the field. (Show on hover)
            },
            "option1", // Default Value
          )
          // ... other fields ...
  ```
