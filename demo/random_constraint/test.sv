// Generator : SpinalHDL v1.13.0    git head : d9d72474863badf47d8585d187f3e04ae4749c59
// Component : test

`timescale 1ns/1ps

module test (
  input  wire          data_in_valid,
  output wire          data_in_ready,
  input  wire [31:0]   data_in_payload,
  output wire          data_out_valid,
  input  wire          data_out_ready,
  output wire [31:0]   data_out_payload,
  input  wire          clk,
  input  wire          reset
);

  wire       [15:0]   _zz_data_in_translated_payload;
  wire                data_in_translated_valid;
  wire                data_in_translated_ready;
  wire       [31:0]   data_in_translated_payload;
  wire                data_in_translated_s2mPipe_valid;
  reg                 data_in_translated_s2mPipe_ready;
  wire       [31:0]   data_in_translated_s2mPipe_payload;
  reg                 data_in_translated_rValidN;
  reg        [31:0]   data_in_translated_rData;
  wire                data_in_translated_s2mPipe_m2sPipe_valid;
  wire                data_in_translated_s2mPipe_m2sPipe_ready;
  wire       [31:0]   data_in_translated_s2mPipe_m2sPipe_payload;
  reg                 data_in_translated_s2mPipe_rValid;
  reg        [31:0]   data_in_translated_s2mPipe_rData;

  assign _zz_data_in_translated_payload = (data_in_payload[15 : 0] + data_in_payload[31 : 16]);
  assign data_in_translated_valid = data_in_valid;
  assign data_in_ready = data_in_translated_ready;
  assign data_in_translated_payload = {16'd0, _zz_data_in_translated_payload};
  assign data_in_translated_ready = data_in_translated_rValidN;
  assign data_in_translated_s2mPipe_valid = (data_in_translated_valid || (! data_in_translated_rValidN));
  assign data_in_translated_s2mPipe_payload = (data_in_translated_rValidN ? data_in_translated_payload : data_in_translated_rData);
  always @(*) begin
    data_in_translated_s2mPipe_ready = data_in_translated_s2mPipe_m2sPipe_ready;
    if((! data_in_translated_s2mPipe_m2sPipe_valid)) begin
      data_in_translated_s2mPipe_ready = 1'b1;
    end
  end

  assign data_in_translated_s2mPipe_m2sPipe_valid = data_in_translated_s2mPipe_rValid;
  assign data_in_translated_s2mPipe_m2sPipe_payload = data_in_translated_s2mPipe_rData;
  assign data_out_valid = data_in_translated_s2mPipe_m2sPipe_valid;
  assign data_in_translated_s2mPipe_m2sPipe_ready = data_out_ready;
  assign data_out_payload = data_in_translated_s2mPipe_m2sPipe_payload;
  always @(posedge clk or posedge reset) begin
    if(reset) begin
      data_in_translated_rValidN <= 1'b1;
      data_in_translated_s2mPipe_rValid <= 1'b0;
    end else begin
      if(data_in_translated_valid) begin
        data_in_translated_rValidN <= 1'b0;
      end
      if(data_in_translated_s2mPipe_ready) begin
        data_in_translated_rValidN <= 1'b1;
      end
      if(data_in_translated_s2mPipe_ready) begin
        data_in_translated_s2mPipe_rValid <= data_in_translated_s2mPipe_valid;
      end
    end
  end

  always @(posedge clk) begin
    if(data_in_translated_ready) begin
      data_in_translated_rData <= data_in_translated_payload;
    end
    if(data_in_translated_s2mPipe_ready) begin
      data_in_translated_s2mPipe_rData <= data_in_translated_s2mPipe_payload;
    end
  end


endmodule
