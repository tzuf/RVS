# Check the types in everything.
pytype rvs

# Build everything
bazel query rvs/... | xargs bazel build
