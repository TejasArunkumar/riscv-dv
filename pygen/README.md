This README file contains commands to help you run assembly generation for Zicond and Zcb extensions.

To run Zicond test:

    python3 run.py --test riscv_zicond_test --simulator=pyflow --target=rv64imafdcZicond -o zicond_test_run

to run Zcb test:

    python3 run.py --test riscv_zcb_test --simulator=pyflow --target=rv64imcZcb --steps=gen -o zcb_test_run

Note: No GCC support for Zcb yet