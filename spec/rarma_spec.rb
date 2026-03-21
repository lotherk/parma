require 'spec_helper'

describe Rarma do
  it 'has a version number' do
    expect(Rarma::VERSION).not_to be nil
  end

  it 'has a logger' do
    expect(Rarma.logger).not_to be nil
  end
end