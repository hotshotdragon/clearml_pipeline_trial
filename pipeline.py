def executing_pipeline(pickle_url):
    print('Pipeline Args:',pickle_url)

    print('launch step 2')

    X_train, X_test, y_train, y_test = step_two(pickle_url)

    print('launch step 3')

    X_train, encoder = step_three(X_train)

    print('launch step 4')

    model = step_four(X_train,y_train)

    print('returned model: {}'.format(model))

    print('launch step four')
    
    accuracy = 100 * step_five(model, X_test, y_test, encoder)
    print(f"Accuracy={accuracy}%")